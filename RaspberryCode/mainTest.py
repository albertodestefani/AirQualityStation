
# read the coordinates from the temp file 
from gps_test.coordinates import CoordinatesConverter


filepath ="../../temp/coordinates.txt"

try:
    with open(filepath, 'r') as file:
        content = file.read()
        coordinates = content.split()  # Split the string

        latitude = float(coordinates[0])
        longitude = float(coordinates[1])

        print("Latitude:", latitude)
        print("Longitude:", longitude)
except FileNotFoundError:
    print("Error: file not exists")
except PermissionError:
    print("Error: No permission on the file")
except Exception as e:
    print(f"Error: {e}")

    
import requests

class Geocoder:
    def reverse_geocode(self, latitude, longitude):
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&accept-language=it&addressdetails=1"
            response = requests.get(url)
            response.raise_for_status()  # Verifica per errori HTTP
            data = response.json()
            
            address = data.get('address', {})

            # Costruzione della stringa location con verifica delle chiavi
            road = address.get('road', '')
            town = address.get('town', '')
            county = address.get('county', '')
            state = address.get('state', '')
            country = address.get('country', '')

            self.location = f"{data.get('lat', '')}, {data.get('lon', '')}, {road}, {town}, {county}, {state}, {country}"
            
            tupla = {
                "latitude": data.get('lat', ''),
                "longitude": data.get('lon', ''),
                "road": road, 
                "town": town, 
                "county": county, 
                "state": state, 
                "country": country
            }
            
            return tupla
        except requests.RequestException as e:
            print(f"HTTP error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

geocoder = Geocoder()
try:
    # Get the address by converting the coordinates
    location = geocoder.reverse_geocode(latitude, longitude)
    print(location)  
    if location is None:
        raise ValueError("Coordinates conversion didn't work")
except ValueError as e:
    print(e)
    exit()

