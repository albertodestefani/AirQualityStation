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
        cursor.execute("SELECT * FROM locations")
        rows = cursor.fetchall()

        id = None

        for row in rows:
            # array temporaneo senza id per verificare uguaglianza
            temp_row = row[1:]

            if np.array_equal(temp_row, location):
                id = row[0]
                print("ID location: ", id)

        if id is None:
            print("Location non presente nel db, creazione di una nuova istanza ...")

            sql = "INSERT INTO locations (road_address, city, province, region, country) VALUES (%s, %s, %s, %s, %s)"
            val = (
                location['road'], 
                location['town'], 
                location['county'], 
                location['state'], 
                location['country']
            )

            cursor.execute(sql, val)
            mydb.commit()
    
            # assegna id successivo
            id = len(rows) + 1

        # Close cursor and databese connection for internet saving
        cursor.close()
        mydb.close()

        return id

    
