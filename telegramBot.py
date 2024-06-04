import json
import logging
import subprocess
import asyncio
import datetime
import time
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from RaspberryCode.readData import ReadData
from RaspberryCode.gps_test.coordinates import CoordinatesConverter 

# Set the DEBUG variable to enable/disable debug messages
DEBUG = 1
printer = ReadData()
# Get the timezone of our area
now = datetime.datetime.now(pytz.timezone("Europe/Rome")) 
date_start = now.strftime('%Y-%m-%d %H:%M')
# Global coordinates variable
latitude = 0
longitude = 0
# coordinates set
setCoordinates = False

# Function to get the bot token from a JSON file
def getToken():
    try:
        # Open the JSON file containing the token
        with open('../conn/telegramBot.json', 'r') as json_file:
            data = json.load(json_file)
        token = data['token']
        return token
    except Exception as e:
        # Handle any errors during token loading
        print(f"Error loading the token: {e}")
        exit(1)

# Error handler for the bot
def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(f'Exception {context.error} occurred while processing update {update}')

# Function to get the PID from a file
def getPID():
    try:
        with open("RaspberryCode/temp/pid.txt", "r") as file:
            pid = file.read()
            return pid if pid else None
    except subprocess.CalledProcessError:
        return None
    
# Async function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! This bot monitors the AQS station, an air quality detector in the municipality of Vittorio Veneto. \nUse /start_detection to start detection and /stop_detection to stop it. \nUse /get_coordinates to read the coordinates and /get_location to convert them into an address.")

# Async function to handle the /start_detection command
async def start_detection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if getPID() is None:
        await update.message.reply_text('Starting detection... Please wait 30 seconds')
        subprocess.Popen(["python3", "RaspberryCode/main.py"]) # Start detection asynchronously
    else:
        await update.message.reply_text('Detection already in progress...')

# Async function to handle the /website command
async def website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Website with the complete history of detections:\n http://www.comunevittorioveneto.it/airqualitystation/')

# Async function to handle the /reset command
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Resetting temporary files")
    subprocess.run(['truncate', '-s', '0', 'RaspberryCode/temp/numberOfReadings.txt'])
    subprocess.run(['truncate', '-s', '0', 'RaspberryCode/temp/pid.txt'])
    subprocess.run(['truncate', '-s', '0', 'RaspberryCode/temp/coordinates.txt'])

# Async function to handle the /get_coordinates command
async def coordinates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global latitude, longitude, setCoordinates
    await update.message.reply_text("Detecting coordinates")
    subprocess.run(["./RaspberryCode/getCoordinates.sh"], check=True)
    time.sleep(10)

    try:
        with open("RaspberryCode/temp/coordinates.txt") as file:
            data = file.read()

            if data != '':
                await update.message.reply_text(data)
                coordinates = data.split()  # Split the string
                latitude = float(coordinates[0])
                longitude = float(coordinates[1])
                setCoordinates = True
            else:
                await update.message.reply_text("Error! Coordinates not detected... Try again later")
    except FileNotFoundError:
        logging.error("File not found")

# Async function to handle the /get_location command
# Used to trasform coordinates into an address
async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global latitude, longitude, converter, setCoordinates

    if setCoordinates:
        converter.reverse_geocode(latitude, longitude)
        address = converter.get_string()
        await update.message.reply_text(address)
    else:
        await update.message.reply_text("It seems like you are asking for coordinates that have not yet been retrieved. Please use the /get_coordinates command to retrieve them.")


# Async function to handle the /stop command (Linux-like systems)
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pid = getPID()
    if pid:
        # Use subprocess to send the termination signal
        process = await asyncio.create_subprocess_shell(f"kill {pid}")
        await process.communicate()
        # process = await asyncio.create_subprocess_shell(f"taskkill /PID {pid} /F")
        await update.message.reply_text('Detection stopped... sending data...')

        # Uncomment and adjust this section to send a PDF report
        date_end = now.strftime('%Y-%m-%d %H:%M')
        pdfPath = printer.getPDF(date_start, date_end)
        print("PDF path: ", pdfPath)

        if pdfPath:
            await update.message.reply_document(document=open(pdfPath, 'rb'))
        else:
            await update.message.reply_text('Error generating the PDF.')
    else:
        await update.message.reply_text('No detection in progress.')

converter = CoordinatesConverter()  

# Main function to configure and start the bot
def main():
    TOKEN = getToken()  # Get the bot token

    # Configure logging for debug and info messages
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Create the Application object using the bot token
    application = Application.builder().token(TOKEN).build()
    application.add_error_handler(error_handler)

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_detection", start_detection))
    application.add_handler(CommandHandler("stop_detection", stop))
    application.add_handler(CommandHandler("website", website))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("get_coordinates", coordinates))
    application.add_handler(CommandHandler("get_location", location))

    # Start the bot in polling mode to receive messages
    application.run_polling()

    
# Execute the main function if the script is run directly
if __name__ == "__main__":
    main()
