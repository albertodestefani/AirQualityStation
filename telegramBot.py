import json
import logging
import subprocess
import asyncio
import datetime
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from RaspberryCode.readData import ReadData


# Imposta la variabile DEBUG per attivare/disattivare i messaggi di debug
DEBUG = 1
printer = ReadData()
# Get the timezone of our area
now = datetime.datetime.now(pytz.timezone("Europe/Rome")) 
date_start = now.strftime('%Y-%m-%d %H:%M')

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

def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(f'Exception {context.error} occurred while processing update {update}')


def getPID():
    try:
        with open("RaspberryCode/temp/pid.txt", "r") as file:
            pid = file.read()
            return pid if pid else None
    except subprocess.CalledProcessError:
        return None
    
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ciao! Questo bot controlla la stazione AQS, rilevatore di qualità dell'aria nel comune di Vittorio Veneto. \nUtilizza /start_detection per iniziare la rilevazione e /stop_detection per terminarla.")

# Funzione asincrona per gestire il comando /start
async def start_detection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if getPID() == None:
        await update.message.reply_text('Avvio della rilevazione... Attendere 30 secondi')
        subprocess.Popen(["python3", "RaspberryCode/main.py"]) #in modo asincrono
    else:
        await update.message.reply_text('Rilevazione già in corso...')

async def website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Sito web dove trovare lo storico completo delle rilevazioni:\n http://www.comunevittorioveneto.it/airqualitystation/')

# Funzione asincrona per gestire il comando /stop --> valida per sistemi linux-like
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pid = getPID()
    if pid:
        # Usa subprocess per inviare il segnale di terminazione
        process = await asyncio.create_subprocess_shell(f"kill {pid}")
        await process.communicate()
        await update.message.reply_text('Rilevazione terminata... invio dei dati...')

        date_end = now.strftime('%Y-%m-%d %H:%M')
        pdfPath = printer.getPDF(date_start, date_end)

        filepath = subprocess.run(["python3", "RaspberryCode/readData.py"], capture_output=True, text=True)
        if filepath:
            await update.message.reply_document(document=open(pdfPath, 'rb'))
        else:
            await update.message.reply_text('Errore nella generazione del PDF.')
    else:
        await update.message.reply_text('Nessuna rilevazione in corso.')

# Funzione valida solo per sistemi windows (test)
# async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     pid = getPID()
#     if pid:
#         process = await asyncio.create_subprocess_shell(f"taskkill /PID {pid} /F")
#         await process.communicate()
#         await update.message.reply_text('Rilevazione terminata... invio dei dati...')
#     else:
#         await update.message.reply_text('Nessuna rilevazione in corso.')

#     data = subprocess.run(["python", "RaspberryCode/temp/readData.py"], capture_output=True, text=True)
#     if data.stdout.strip():
#         await update.message.reply_text(data.stdout)
#     else:
#         await update.message.reply_text('Nessun dato disponibile.') 

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
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("start_detection", start_detection))
    application.add_handler(CommandHandler("stop_detection", stop))
    application.add_handler(CommandHandler("website", website))

    # Avvia il bot in modalità polling per ricevere messaggi
    application.run_polling()

# Esegui la funzione main se lo script viene eseguito direttamente
if __name__ == "__main__":
    main()
