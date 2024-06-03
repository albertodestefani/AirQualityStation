# Questa classe permette di trasformare le coordinate gps in indirizzo da poter 
# salvare nel db, utiliza un servizio chiamato "nominatim.openstreetmap.org",
# il programma manda una request HTTP e l'host ritorna dei dati in formato json
# il programma va poi a fare una cernita dei dati per costruire una stringa 

import requests

class CoordinatesConverter:   
    # We use this to have full control over the response
    # Returns a tuple containing essential data

    def __init__(self) -> None:
        pass

    def reverse_geocode(self, latitude, longitude):
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            
            address = data['address']

            # String that can be printed for error checking
            self.location = address['road'] + ', ' + address['town'] + ', ' + address['county'] + ', ' + address['state'] + ', ' + address['country']

            # Create a formatted tuple with selected data to return
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



# # test
# converter = CoordinatesConverter()
# # 45.99755068 12.291252627
# # 45.997566111  12.290824468
# datas = converter.reverse_geocode(45.997486149, 12.291401648)
# print(datas)