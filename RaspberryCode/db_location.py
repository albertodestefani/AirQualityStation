import json
import mariadb
import mysql.connector
import sys
from Haversine import HaversineCalculator

# This object searches the database for the location ID if it is already saved.
# If it doesn't exist, it creates it with an SQL query.
# Returns the ID.

class DB_Location:
    def __init__(self):
        # Load database connection data from a JSON file
        with open('../conn/connection_data.json', 'r') as json_file:
            self.data = json.load(json_file)

    # Function to insert a new location into the database
    def insertLocation(cursor, location):
        sql = "INSERT INTO locations (road_address, city, province, region, country, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, location)
        
    # Function to get the ID of a location
    def getId(self, location):
        haversine = HaversineCalculator()

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
            # Create connection to the database
            mydb = mysql.connector.connect(
                user=self.data['user'],
                password=self.data['password'],
                host=self.data['host'],
                port=self.data['port'],
                database=self.data['database'],
            )
        except mariadb.Error as e:
            # Handle database connection errors
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cursor = mydb.cursor()
        query = "SELECT * FROM locations"
        cursor.execute(query)

        try:
            datas = cursor.fetchall()
        except Exception as e:
            # Handle errors when fetching data
            print("Database is empty...")
            print("Inserting location into the database")
            self.insertLocation(cursor, location)
            return cursor.lastrowid

        for data in datas:
            # Precise location check
            tupla = tuple(item for index, item in enumerate(data) if index not in (0, 6, 7))
            coordinates_tupla = tuple(item for index, item in enumerate(data) if index in (6, 7))
            if tupla == val:
                return data[0]
            # Otherwise, check for rounding
            else:
                if haversine.coordinatesInRange(coordinates, coordinates_tupla, 100): # radius = 100
                    return data[0]

        # If rounding was not possible, insert the location into the database
        self.insertLocation(cursor, location)
        id = cursor.lastrowid 

        # Close the database connection to save resources
        mydb.close()
        return id

# Example usage:
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
