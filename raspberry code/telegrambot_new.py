"""import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = ""

def start(update, context):
    update.message.reply_text("Ciao sono AQS, invia il messaggio 'avvia' per eseguire una rilevazione")

def comando(update, context):
    testo = update.message.text.lower()
    if "avvia" in testo:
        os.system("python3 main.py")
        update.message.reply_text("Avvio della AirQualityStation")
    else:
        update.message.reply_text("Comando non trovato")

updater = Updater(TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, comando))
print("bot in ascolto ...")
updater.start_polling()"""

import json
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

#estrazione token
def getToken():
    with open('../conn/telegramBot.json', 'r') as json_file:
        data = json.load(json_file)
    token = data['token']
    return token

#comandi
#start per avviare il bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Benvenuto! Usa /start_detection per avviare la rilevazione e /show_website per vedere i risultati.')

#comando per avviare la rilevazione
def start_detection(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Avvio della rilevazione in corso...')
    # Qui puoi aggiungere il codice per eseguire lo script di rilevazione
    # subprocess.run(["python", "main.py"])
    update.message.reply_text('Rilevazione avviata!')

#comando per visualizzare il sito web dove vengono messe le rilevazioni
def show_website(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Visita il nostro sito per i risultati della rilevazione: http://example.com')#CAMBIARE INDIRIZZO

#comando per vedere lo stato del raspberry, se acceso o spento
def check_status(update: Update, context: CallbackContext) -> None:
    try:
        # Sostituisci 'indirizzo_ip' con l'IP del tuo Raspberry Pi
        response = subprocess.check_output(['ping', '-c', '1', 'indirizzo_ip'], stderr=subprocess.STDOUT)
        update.message.reply_text('La stazione è attiva!')
    except subprocess.CalledProcessError:
        update.message.reply_text('La stazione è attualmente spenta.')

def main() -> None:
    # Inserisci il token del tuo bot qui
    TOKEN = getToken()
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher
    
    #per far funzionare i comandi
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("start_detection", start_detection))
    dispatcher.add_handler(CommandHandler("show_website", show_website))
    dispatcher.add_handler(CommandHandler("check_status", check_status))
# boh
    updater.start_polling()
    updater.idle()
#boh
if __name__ == '__main__':
    main()