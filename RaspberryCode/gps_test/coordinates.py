# Questa classe permette di trasformare le coordinate gps in indirizzo da poter 
# salvare nel db, utiliza un servizio chiamato "nominatim.openstreetmap.org",
# il programma manda una request HTTP e l'host ritorna dei dati in formato json
# il programma va poi a fare una cernita dei dati per costruire una stringa 

# attualmente la funzione coordinates_to_address non è utilizzata perchè non permette di costruire la stringa a piacimento


#pip install geopy
from geopy.geocoders import Nominatim
import requests

class CoordinatesConverter:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="gps_converter")

    def coordinates_to_address(self, latitude, longitude):
        # Combina le coordinate
        coordinates = f"{latitude}, {longitude}"

        try:
            # Ottieni l'indirizzo corrispondente alle coordinate
            location = self.geolocator.reverse(coordinates, language='it')
            print(f"Coordinate: {coordinates}")
            # print(f"Indirizzo: {location.address}")
            return location.address
        except Exception as e:
            print(f"Errore durante la conversione delle coordinate: {e}")
            return None
        
    # usiamo questo per avere una gestione completa della response
    # ritorna una tupla contenente dati essenziali
    def reverse_geocode(self, latitude, longitude):
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&accept-language=it&addressdetails=1"
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            
            address = data['address']

            # stringa da poter stampare come check error
            self.location = data['lat'] + data['lon'] + address['road'] + ', ' + address['town'] + ', ' + address['county'] + ', ' + address['state'] + ', ' + address['country']

            tupla = {
                "latitude": data['lat'],
                "longitude": data['lon'],
                "road": address['road'], 
                "town": address['town'], 
                "county": address['county'], 
                "state": address['state'], 
                "country": address['country']
            }
            
            return tupla
        except requests.RequestException as e:
            print(f"HTTP error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        
    def get_string(self):
        return self.location
        


# test
converter = CoordinatesConverter()
# 45.99755068 12.291252627
# 45.997566111  12.290824468
datas = converter.reverse_geocode(45.997486149, 12.291401648)
print(datas)