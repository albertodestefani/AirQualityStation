# Rilevazione delle coordinate e scrittura su file temporaneo
gpspipe -w -n 10 | grep -m 1 -oP '"lat":\K[-\d.]+|(?<="lon":)[-\d.]+' | tr '\n' ' ' > coordinates.txt

# Avvio del main
python3 main.py

# creare il demone con systemd 
