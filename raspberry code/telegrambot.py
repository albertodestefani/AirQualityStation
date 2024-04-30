import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "7134224901:AAGBSx9GwrYduwTUTNueRX6N4FDluf-cV2Q"

def start(update, context):
    update.message.reply_text("Ciao sono AQS, invia il messaggio '/avvia' per eseguire una rilevazione")

def comando(update, context):
    testo = update.message.text.lower()
    if "/avvia" in testo:
        os.system("python3 main.py")
        update.message.reply_text("Avvio della AirQualityStation")
    else:
        update.message.reply_text("Comando non trovato")

updater = Updater (TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, comando))
print("bot in ascolto ...")
updater.start_polling()