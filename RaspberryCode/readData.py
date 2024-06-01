import requests
import os

class ReadData:
    def __init__(self, readings_file="RaspberryCode/temp/numberOfReadings.txt", pdf_output="RaspberryCode/temp/readings.pdf"):
        self.readings_file = readings_file
        self.pdf_output = pdf_output
    
    # Function to read the number of readings from a file
    def getNumberOfReadings(self):
        try:
            with open(self.readings_file, 'r') as file:
                data = file.read()
                return data if data else None
        except FileNotFoundError:
            print(f"Error: The file {self.readings_file} does not exist.")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    # Function to fetch a PDF report from a given date range
    def getPDF(self, date_start, date_end):
        i = self.getNumberOfReadings()
        if not i:
            print("Error: Invalid number of readings.")
            return None
        
        try:
            # Construct the URL to request the PDF
            url = f"http://www.comunevittorioveneto.it/airqualitystation/getPDF.php?readings_from={date_start}&readings_to={date_end}&order_by=date_time&desc=DESC&n={i}&mode=true"
            # testURL = "https://zsory-furdo.hu/evcms_medias/upload/files/testfile.pdf"  # For testing
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            
            # Save the response content as a PDF file
            with open(self.pdf_output, "wb") as file:
                file.write(response.content)
            
            if os.path.getsize(self.pdf_output) == 0:
                print("Error: The PDF file is empty.")
                return None
            
            print(f"PDF saved as {self.pdf_output}")
            return self.pdf_output
        except requests.RequestException as e:
            print(f"HTTP error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
