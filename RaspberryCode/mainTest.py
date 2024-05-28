import os


def main():
    i=0

    # Apri il file in modalità scrittura ('w' sta per write)
    with open("RaspberryCode/temp/pid.txt", "w") as file:
        # Scrivi nel file
        pid = os.getpid()
        file.write(str(pid))

    while(True):
        i = i+1
    


if __name__ == "__main__":
    main()