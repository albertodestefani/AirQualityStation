#!/bin/bash
# Rilevazione delle coordinate e scrittura su file temporaneo

# Esegui il comando gpspipe e cattura l'output
output=$(gpspipe -w -n 10 | grep -m 1 -oP '"lat":\K[-\d.]+|(?<="lon":)[-\d.]+' | tr '\n' ' ')

# Verifica lo stato di uscita del comando gpspipe
if [ $? -ne 0 ]; then
    echo "Errore durante l'esecuzione di gpspipe" >&2
    exit 1
fi

# Verifica se l'output è vuoto
if [ -z "$output" ]; then
    echo "Nessuna coordinata trovata" >&2
    exit 1
fi

# Scrivi l'output nel file coordinates.txt
echo "$output" > RaspberryCode/temp/coordinates.txt

# Verifica lo stato di uscita del comando di scrittura su file
if [ $? -ne 0 ]; then
    echo "Errore durante la scrittura del file coordinates.txt" >&2
    exit 1
fi

# Avvio del main
# python3 ../TelegramBot/telegramBot.py


