import requests
import os

class ReadData:
    def __init__(self, readings_file="RaspberryCode/temp/numberOfReadings.txt", pdf_output="RaspberryCode/temp/readings.pdf"):
        self.readings_file = readings_file
        self.pdf_output = pdf_output
    
    def getNumberOfReadings(self):
        try:
            with open(self.readings_file, 'r') as file:
                data = file.read()
                return data if data else None
        except FileNotFoundError:
            print(f"Errore: il file {self.readings_file} non esiste.")
            return None
        except Exception as e:
            print(f"Errore imprevisto: {e}")
            return None

    def getPDF(self, date_start, date_end):
        i = self.getNumberOfReadings()
        if not i:
            print("Errore: numero di letture non valido.")
            return None
        
        try:
            url = f"http://www.comunevittorioveneto.it/airqualitystation/getPDF.php?readings_from={date_start}&readings_to={date_end}&order_by=date_time&desc=DESC&n={i}&mode=true"
            # testURL = "https://zsory-furdo.hu/evcms_medias/upload/files/testfile.pdf"  # Per testare
            response = requests.get(url)
            response.raise_for_status()  # Controlla eventuali errori HTTP
            
            # Salva il contenuto della risposta come file PDF
            with open(self.pdf_output, "wb") as file:
                file.write(response.content)
            
            if os.path.getsize(self.pdf_output) == 0:
                print("Errore: il file PDF è vuoto.")
                return None
            
            print(f"PDF salvato come {self.pdf_output}")
            return self.pdf_output
        except requests.RequestException as e:
            print(f"Errore HTTP: {e}")
            return None
        except Exception as e:
            print(f"Errore imprevisto: {e}")
            return None

