# oggetto che cerca nel db l'id della location se è gia salvata
# se non esiste la crea con una query SQL
# ritorna id 

import json
import mariadb
import mysql.connector
import sys
import numpy as np


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
            print("fError connecting to MariaDB Platform: {e}")
            sys.exit(1)

        cursor = mydb.cursor()
        query = "SELECT * FROM locations WHERE (road_address = %s) AND (city = %s) AND (province = %s) AND (region = %s) AND (country = %s)"
        cursor.execute(query, val)
        
        try:
            row = cursor.fetchone()
            print(row)
            id = row['id']
            print("ID location: ", id)
        except Exception as e:
            print("Location non presente nel db, creazione di una nuova istanza ...")

            sql = "INSERT INTO locations (road_address, city, province, region, country) VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(sql, val)
            mydb.commit()
    
            # assegna id successivo
            """""
            nel caso in cui venga scelto di realizzare nuove stazioni che lavorano in contemporanea
            questa funzione è da riadattare perche potrebbero essere eseguite più query nello stesso momento
            con risultante di un lastrowid inserito errato
            """""
            id = cursor.lastrowid
            print("nuovo id: ", id)

        # Close cursor and databese connection for internet saving
        cursor.close()
        mydb.close()

        return id

    
