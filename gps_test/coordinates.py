#pip install geopy
from geopy.geocoders import Nominatim

# def coordinates_to_address(latitude, longitude):
#     # Inizializza il geolocatore Nominatim
#     geolocator = Nominatim(user_agent="gps_converter")

#     # Combina le coordinate
#     coordinates = f"{latitude}, {longitude}"

#     try:
#         # Ottieni l'indirizzo corrispondente alle coordinate
#         location = geolocator.reverse(coordinates, language='it')
#         print(f"ciao: {location.address}")

#         # Stampa l'indirizzo
#         print(f"Coordinate: {coordinates}")
#         print(f"Indirizzo: {location.address}")
#     except Exception as e:
#         print(f"Errore durante la conversione delle coordinate: {e}")


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
            print(f"Indirizzo: {location.address}")
            return location.address
        except Exception as e:
            print(f"Errore durante la conversione delle coordinate: {e}")
            return None

# Esempio di utilizzo
# latitude = 45.9969722
# longitude = 12.291138888888888

# coordinates_to_address(latitude, longitude)
