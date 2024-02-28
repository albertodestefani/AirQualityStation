#pip install geopy
from geopy.geocoders import Nominatim

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
