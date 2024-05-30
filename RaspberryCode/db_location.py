# oggetto che cerca nel db l'id della location se è gia salvata
# se non esiste la crea con una query SQL
# ritorna id 

import json
import mariadb
import mysql.connector
import sys
from Haversine import HaversineCalculator

class DB_Location:
    def __init__(self):
        with open('../../conn/connection_data.json', 'r') as json_file:
            self.data = json.load(json_file)

    def insertLocation(cursor, location):
        sql = "INSERT INTO locations (road_address, city, province, region, country, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, location)
        
    def getId(self, location):
        haversine = HaversineCalculator();

        val = (
            location['road'], 
            location['town'], 
            location['county'], 
            location['state'], 
            location['country']
        )
        coordinates = {
            'latitude': location['latitude'],
            'longitude': location['longitude']
        }

        try:
            # Create connection to Database
            mydb = mysql.connector.connect(
                user = self.data['user'],
                password = self.data['password'],
                host = self.data['host'],
                port = self.data['port'],
                database = self.data['database'],
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cursor = mydb.cursor()
        query = "SELECT * FROM locations"
        cursor.execute(query)

        try:
            datas = cursor.fetchall()
        except Exception as e:
            print("Database vuoto...")
            print("Inserimento della location nel db")
            self.insertLocation(cursor, location)
            return cursor.lastrowid

        for data in datas:
            # controllo della locazione precisa
            tupla = tuple(item for index, item in enumerate(data) if index not in (0, 6, 7))
            coordinates_tupla = tuple(item for index, item in enumerate(data) if index in (6, 7))
            if tupla == val:
                return data[0]
            # altrimenti cerca un arrotondamento
            else:
                if(haversine.coordinatesInRange(coordinates, coordinates_tupla, 100)): # raggio = 100
                    return data[0]

        # se non è stato possibile un arrotondamento inserisce la location nel db
        self.insertLocation(cursor, location)
        id = cursor.lastrowid 

        # Close databese connection for internet saving
        mydb.close()
        return id

    
# db = DB_Location()
# location = {
#     "road": "Via Piai", 
#     "town": "Vittorio Veneto", 
#     "county": "Treviso", 
#     "state": "Veneto", 
#     "country": "Italia"
# }
# id = db.getId(location)
# print(id)
