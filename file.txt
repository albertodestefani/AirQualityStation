gpspipe -w -n 10 | grep -m 1 -oP '"lat":\K[-\d.]+|(?<="lon":)[-\d.]+' | tr '\n' ' ' > coordinates.txt
python3 main.py

# creare il demone con systemd 
