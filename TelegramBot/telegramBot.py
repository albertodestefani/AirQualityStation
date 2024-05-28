import json
import logging
import os
import subprocess
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

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

def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.error(f'Exception {context.error} occurred while processing update {update}')


def getPID():
    try:
        with open("RaspberryCode/temp/pid.txt", "r") as file:
            pid = file.read()
            return pid if pid else None
    except subprocess.CalledProcessError:
        return None

# Funzione asincrona per gestire il comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if getPID() == None:
        await update.message.reply_text('Avvio della rilevazione...')
        # subprocess.Popen(["python3", "RaspberryCode/mainTest.py"]) #in modo asincrono
        subprocess.Popen(["python3", "RaspberryCode/main.py"]) #in modo asincrono
    else:
        await update.message.reply_text('Rilevazione già in corso... Attendere')

# Funzione asincrona per gestire il comando /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pid = getPID()
    if pid:
        # Usa subprocess per inviare il segnale di terminazione
        process = await asyncio.create_subprocess_shell(f"kill {pid}")
        await process.communicate()
        await update.message.reply_text('Rilevazione terminata... invio dei dati...')
    
        data = subprocess.run(["python3", "RaspberryCode/temp/readData.py"], capture_output=True, text=True)
        if data.stdout.strip():
            await update.message.reply_text(data.stdout)
        else:
            await update.message.reply_text('Nessun dato disponibile.')
    else:
        await update.message.reply_text('Nessuna rilevazione in corso.')

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
    application.add_handler(CommandHandler("start_detection", start))
    application.add_handler(CommandHandler("stop_detection", stop))

    # Avvia il bot in modalità polling per ricevere messaggi
    application.run_polling()

# Esegui la funzione main se lo script viene eseguito direttamente
if __name__ == "__main__":
    main()
