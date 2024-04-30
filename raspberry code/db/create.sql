CREATE TABLE locations (
id INTEGER AUTO_INCREMENT NOT NULL,
road_address VARCHAR(30) NOT NULL,
city VARCHAR(50) NOT NULL,
province VARCHAR(50) NOT NULL,
region VARCHAR(50) NOT NULL,
country VARCHAR(50) NOT NULL,
latitude POINT NOT NULL,
longitude POINT NOT NULL,
PRIMARY KEY (id)
);

ALTER TABLE locations 
ADD COLUMN latitude GEOGRAPHY NOT NULL,
ADD COLUMN longitude GEOGRAPHY NOT NULL

ALTER TABLE readings
ADD COLUMN id_location INTEGER,
ADD CONSTRAINT fk_id_location FOREIGN KEY (id_location) REFERENCES locations(id);

-- Aggiungi le colonne
ALTER TABLE readings
ADD COLUMN locations_city_name VARCHAR(255),
ADD COLUMN locations_city_address VARCHAR(255);

-- Aggiungi i vincoli di chiave esterna
ALTER TABLE readings
ADD CONSTRAINT fk_city_name FOREIGN KEY (locations_city_name) REFERENCES locations(city_name),
ADD CONSTRAINT fk_city_address FOREIGN KEY (locations_city_address) REFERENCES locations(city_address);
