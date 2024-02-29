# oggetto che cerca nel db l'id della location se è gia salvata
# se non esiste la crea con una query SQL
# ritorna id 

import json
import mariadb
import mysql.connector
import sys


class DB_Location:
    def __init__(self):
        with open('../conn/connection_data.json', 'r') as json_file:
            self.data = json.load(json_file)
        
    def getId(self, location):
        val = (
            location['road'], 
            location['town'], 
            location['county'], 
            location['state'], 
            location['country']
        )

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
        query = "SELECT * FROM locations WHERE (road_address = %s) AND (city = %s) AND (province = %s) AND (region = %s) AND (country = %s)"
        cursor.execute(query, val)
        
        try:
            row = cursor.fetchone()
            
            print(row)
            id = row[0]
            print("ID location: ", id)
        except Exception as e:
            print("Location non presente nel db, creazione di una nuova istanza ...")

            sql = "INSERT INTO locations (road_address, city, province, region, country) VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(sql, val)

            # assegna id successivo
            """""
            nel caso in cui venga scelto di realizzare nuove stazioni che lavorano in contemporanea
            questa funzione è da riadattare perche potrebbero essere eseguite più query nello stesso momento
            con risultante di un lastrowid inserito errato
            """""
            id = cursor.lastrowid
            print("nuovo id: ", id)

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