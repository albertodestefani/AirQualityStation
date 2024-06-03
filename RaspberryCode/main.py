# Module Imports
import os
import requests
import ST7735
from bme280 import BME280
from enviroplus import gas
from pms5003 import PMS5003, ReadTimeoutError, ChecksumMismatchError
import mariadb
import mysql.connector
import sys
import datetime
import pytz
import time
import math as m
import json
import asyncio
from telegram import Bot
from Noise import Noise
from gps_test.coordinates import CoordinatesConverter
from db_location import DB_Location

# Tutti i percorsi dei file sono relativi a telegramBot.py

# Progressive bar
from time import sleep
from tqdm import tqdm

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

import logging
#format for the message that you see when a detection is made
logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

# Create I2C canal connection
bus = SMBus(1)

# Create BME280 instance
bme280 = BME280(i2c_dev=bus)

# Create PMS5003 instance
pms5003 = PMS5003()

# Set up sound settings
spl_ref_level = 0.000001 # Sets quiet level reference baseline for dB(A) measurements. alsamixer at 10
spl_thresholds = (70, 90)
log_sound_data = True # Set to True to log sound data for debugging
debug_recording_capture = False # Set to True for plotting each recording stream sample

#Noise object must be instanciated in the loop

#Antoinconstants for Water to calculate vapor pressure or boiling temperature
AntA=18.88579
AntB=-3994.017
AntC=233.874

# Calculate vapor pressure at T of water using Antoine equation
def pvap(T):
    pv=m.exp(AntA-(AntB/(T+AntC)))
    return pv

# Calculate boiling temperature of water using Antoine equation
def tboil(pres):
    tboil=AntB/(m.log(pres)-AntA)-AntC
    return tboil

# Function that read the values from the bme280, the pms5003 and the enviro board
def read_values():
    # Create array for contains values
    values = {}
    
    noise = Noise(spl_ref_level, log_sound_data, debug_recording_capture)
      
    # Get cpu temperature and external temperature
    cpu_temp = get_cpu_temperature()
    raw_temp = bme280.get_temperature()
    # Get the correct temperature adjusting raw temperature with the CPU temperature
    comp_temp = raw_temp - ((cpu_temp - raw_temp) /comp_factor)
    raw_humid = bme280.get_humidity()
    dew_point = tboil(raw_humid / 100 * pvap(raw_temp)) # humid is in %, devide by 100 to get factor 
    # Humidity correction 
    humidity = raw_humid * pvap(raw_temp) / pvap(comp_temp)
    # Get the detection and put it insiede the array
    values["temperature"] = int(comp_temp)
    values["air_pressure"] = int(bme280.get_pressure() * 100)
    values["humidity"] = int(humidity)
    values["Reducing"] = gas.read_reducing()
    values["Oxidising"] = gas.read_oxidising()
    values["NH3"] = gas.read_nh3()
    values["dBA"] = int(noise.spl())

    try:
        #Get supported pollution type values
        pm_values = pms5003.read()
        values["PM1"] = int(pm_values.pm_ug_per_m3(1))
        values["PM25"] = int(pm_values.pm_ug_per_m3(2.5))
        values["PM10"] = int(pm_values.pm_ug_per_m3(10))
    except(ReadTimeoutError, ChecksumMismatchError):
        logging.info("Failed to read PMS5003. Reseting and retrying.")
        pms5003.reset()
        #pm_values = pms5003.read()
        #values["PM1"] = int(pm_values.pm_ug_per_m3(1))
        #values["PM25"] = int(pm_values.pm_ug_per_m3(2.5))
        #values["PM10"] = int(pm_values.pm_ug_per_m3(10))

    return values

def get_token():
    try:
        with open('../conn/telegramBot.json', 'r') as json_file:
            data = json.load(json_file)
        token = data['token']
        return token
    except Exception as e:
        logging.warning(f"Error loading the token: {e}")
        exit(1)

# Funzione per inviare un messaggio Telegram
async def send_telegram_message(token, chat_id, message):
    bot = Bot(token)
    await bot.send_message(chat_id=chat_id, text=message)

# Open the JSON file and load the database configuration datas
def get_connection_data():
    with open('../conn/connection_data.json', 'r') as json_file: #../../conn/connection_data.json
        data = json.load(json_file)
        return data

# Write readings data in a JSON file (not used)
def writeTempData(data):
    try:
        with open('RaspberryCode/temp/readings_test.json', 'r') as json_file:
            readings = json.load(json_file)
    except FileNotFoundError:
        readings = []
    
    readings.append(data)
    
    with open('RaspberryCode/temp/readings_test.json', 'w') as json_file:
        json.dump(readings, json_file, indent=4)

# Function that saves a readings counter in a temp file to use it for the pdf generation 
def setCounter(i):
    with open("RaspberryCode/temp/numberOfReadings.txt", "w") as file:
        # Scrivi nel file
        file.write(str(i))   

# Function that resets the readings counter
def resetCounter():
    with open("RaspberryCode/temp/numberOfReadings.txt", "w") as file:
        # Scrivi nel file
        file.write('')  
 
# Function that saves the main.py PID to kill the process in the telegram bot
def setPID():
    with open("RaspberryCode/temp/pid.txt", "w") as file:
        # Scrivi nel file
        pid = os.getpid()
        file.write(str(pid))

# create the function to get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp
        
# Compensation factor for temperature
comp_factor = 2.8

# read the coordinates from the temp file 
filepath = "RaspberryCode/temp/coordinates.txt"
try:
    with open(filepath, 'r') as file:
        content = file.read()
        coordinates = content.split()  # Split the string

        latitude = float(coordinates[0])
        longitude = float(coordinates[1])

        print("Latitude:", latitude)
        print("Longitude:", longitude)
except FileNotFoundError:
    logging.warning("Error: file not exists")
except PermissionError:
    logging.warning("Error: No permission on the file")
except Exception as e:
    logging.warning(f"Error: {e}")

    
# create the converter object to convert coordinates to address 
converter = CoordinatesConverter()

# create the db_location object to find the location id in the database
db_location = DB_Location()

try:
    # Get the address by converting the coordinates
    location = converter.reverse_geocode(latitude, longitude)  
    if location is None:
        raise ValueError("Coordinates conversion didn't work")
except ValueError as e:
    logging.warning(e)
    exit()

# Counter 
i = 0
# Token
TOKEN = get_token()
# Reset the counter in the temp file
resetCounter()

# Main loop to read data, display, and send to Database
while True:

    try:
        data = get_connection_data()
        # Create connection to Database
        mydb = mysql.connector.connect(
            user = data['user'],
            password = data['password'],
            host = data['host'],
            port = data['port'],
            database = data['database']
            #use_pure=True
        )  
    except mariadb.Error as e:
        logging.warning(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Create a cursor to write on database
    mycursor = mydb.cursor()

    # SQL query creation and execution
    try:
        logging.warning(bme280.get_pressure())
        setPID()
        logging.info("PID set")

        # Trying to read the values for 3 times to get more accurate values
        for i in tqdm(range(3)):
            values = read_values()
            time.sleep(5)
            # logging.info(values)
        logging.info("Reading values")

        # Get the location id
        values['id'] = int(db_location.getId(location) )

        # Get the timezone of our area
        now = datetime.datetime.now(pytz.timezone("Europe/Rome"))
        # For hour with *:00:00 delete %M and %S 
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        # Insert the date 
        values = {"date" : formatted_date, **values}
        print("***** VALUES *****") 
        logging.info(values)    
        # Create the query for the database 
        sql = "INSERT INTO readings (date_time, pm1, pm25, pm10, temperature, humidity, air_pressure, no2, co, nh3, dBA, id_location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (values['date'], values['PM1'], values['PM25'], values['PM10'], values['temperature'], values['humidity'], values['air_pressure'], values['Oxidising'], values['Reducing'], values['NH3'], values['dBA'], values['id'])
        # Execute the SQL query
        mycursor.execute(sql, val)
        #Confirm the changes in the database are made correctly
        mydb.commit()
        logging.info("Query done")
        
    except Exception as e:
        logging.warning('Main Loop Exception: {}'.format(e))   

    # Close cursor and databese connection for internet saving
    mycursor.close()
    mydb.close()

    message = f"New detection completed at {formatted_date}"
    asyncio.run(send_telegram_message(TOKEN, message))

    # Reload counter
    i = i + 1
    setCounter(i)

    # Wait the time for the next detection
    time.sleep(30)
