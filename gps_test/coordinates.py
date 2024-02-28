# Questa classe permette di trasformare le coordinate gps in indirizzo da poter 
# salvare nel db, utiliza un servizio chiamato "nominatim.openstreetmap.org",
# il programma manda una request HTTP e l'host ritorna dei dati in formato json
# il programma va poi a fare una cernita dei dati per costruire una stringa sensata 

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
            # print(f"Coordinate: {coordinates}")
            # print(f"Indirizzo: {location.address}")
            return location.address
        except Exception as e:
            print(f"Errore durante la conversione delle coordinate: {e}")
            return None
        
    # usiamo questo per avere una gestione completa della response
    def reverse_geocode(self, latitude, longitude):
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&accept-language=it&addressdetails=1"
            response = requests.get(url)
            data = response.json()
            address = data['address']
            location = address['road'] + ', ' + address['town'] + ', ' + address['county'] + ', ' + address['state'] + ', ' + address['country']
            return location
        except Exception as e:
            print("error")
            return None


# test
converter = CoordinatesConverter()
# 45.99755068 12.291252627
datas = converter.reverse_geocode(45.99755068, 12.291252627)
print(datas)