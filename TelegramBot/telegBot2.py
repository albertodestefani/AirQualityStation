import json
import logging
import subprocess
import os
from telegram import Update
from telegram.ext import Application, CommandHandler

# Imposta la variabile DEBUG per attivare/disattivare i messaggi di debug
DEBUG = 1

# Funzione per ottenere il token del bot da un file JSON
def getToken():
    try:
        # Apri il file JSON contenente il token
        with open('../conn/telegramBot.json', 'r') as json_file:
            data = json.load(json_file)
        token = data['token']
        return token
    except Exception as e:
        # Gestisce eventuali errori durante il caricamento del token
        print(f"Errore durante il caricamento del token: {e}")
        exit(1)

# Funzione per stampare messaggi di debug
def __debug(msg):
    if DEBUG:
        print("\033[94m[DEBUG]\033[0m", msg)

def error_handler(update, context):
    logging.error(f'Exception {context.error} occurred while processing update {update}')

# Funzione per ottenere l'ID del processo di main.py
def getPID():
    pid = os.popen('pgrep -f "python main.py"').read().strip()
    return pid

# Funzione asincrona per gestire il comando /start
async def start(update: Update, context) -> None:
    if not getPID():
        await update.message.reply_text('Avvio della rilevazione...')
        subprocess.Popen(["python3", "main.py"])
    else:
        await update.message.reply_text('Rilevazione già in corso... Attendere')

# Funzione asincrona per gestire il comando /stop
async def stop(update: Update, context) -> None:
    data = subprocess.run(["python3", "RaspberryCode/temp/readData.py"], capture_output=True, text=True)
    await update.message.reply_text(data.stdout)


# Funzione principale per configurare e avviare il bot
def main():
    TOKEN = getToken()  # Ottiene il token del bot

    # Configura il logging per il debug e le informazioni
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Crea l'oggetto Application usando il token del bot
    application = Application.builder().token(TOKEN).build()
    application.add_error_handler(error_handler)

    # Aggiunge i gestori di comandi
    application.add_handler(CommandHandler("start_detection", start))
    application.add_handler(CommandHandler("stop_detection", stop))

    # Avvia il bot in modalità polling per ricevere messaggi
    application.run_polling()

# Esegui la funzione main se lo script viene eseguito direttamente
if __name__ == "__main__":
    main()
