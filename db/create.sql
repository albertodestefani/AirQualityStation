CREATE TABLE locations (
city_name VARCHAR(30) NOT NULL,
city_address VARCHAR(50) NOT NULL,
longitude FLOAT,
latitude FLOAT,
PRIMARY KEY (city_name, city_address)
);

ALTER TABLE 'readings'
-- DROP COLOUMN luogo,
ADD COLOUMN 'locations_city_name' VARCHAR(30),
ADD COLOUMN 'locations_city_address' VARCHAR(50),
ADD FOREIGN KEY 'locations_city_name' REFERENCES 'locations' ('city_name'),
ADD FOREIGN KEY 'locations_city_address' REFERENCES 'locations' ('city_address');

-- Aggiungi le colonne
ALTER TABLE readings
ADD COLUMN locations_city_name VARCHAR(255),
ADD COLUMN locations_city_address VARCHAR(255);

-- Aggiungi i vincoli di chiave esterna
ALTER TABLE readings
ADD CONSTRAINT fk_city_name FOREIGN KEY (locations_city_name) REFERENCES locations(city_name),
ADD CONSTRAINT fk_city_address FOREIGN KEY (locations_city_address) REFERENCES locations(city_address);
