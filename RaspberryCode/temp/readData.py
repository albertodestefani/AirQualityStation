import json

def main():
    with open('RaspberryCode/temp/readings.json', 'r') as json_file:
        data = json.load(json_file)
        print(data)
    
if __name__ == "__main__":
    main()
        

