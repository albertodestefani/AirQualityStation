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
"""
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

#comandi
#start per avviare il bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Benvenuto! Usa /start_detection per avviare la rilevazione e /show_website per vedere i risultati.')

#comando per avviare la rilevazione
def start_detection(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Avvio della rilevazione in corso...')
    # Qui puoi aggiungere il codice per eseguire lo script di rilevazione
    subprocess.run(["python", "/percorso/dello/script_di_rilevazione.py"])  #CAMBIARE INDIRIZZOOOOOOO
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
    updater = Updater("6584356882:AAGrEAlVGggEmDJZCiXj0-LxZ2HHvk2y0UE") 
    
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
"""

import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler

# IMPORTANTE: inserire il token fornito dal BotFather nella seguente stringa
def start(update, context):
    update.message.reply_text('Benvenuto! Usa /start_detection per avviare la rilevazione e /show_website per vedere i risultati.')

def start_detection(update, context):
    update.message.reply_text('Avvio della rilevazione in corso...')
    # Qui puoi aggiungere il codice per eseguire lo script di rilevazione
    subprocess.run(["python", "/percorso/dello/script_di_rilevazione.py"])  #CAMBIARE INDIRIZZOOOOOOO
    print(f'Rilevazione avviata!')
    #update.message.reply_text('Rilevazione avviata!')

#comando per visualizzare il sito web dove vengono messe le rilevazioni
def show_website(update, context):
    update.message.reply_text('Visita il nostro sito per i risultati della rilevazione: http://example.com')#CAMBIARE INDIRIZZO

#comando per vedere lo stato del raspberry, se acceso o spento
"""def check_status(update, context):
    try:
        # Sostituisci 'indirizzo_ip' con l'IP del tuo Raspberry Pi
        response = subprocess.check_output(['ping', '-c', '1', 'indirizzo_ip'], stderr=subprocess.STDOUT)
        update.message.reply_text('La stazione è attiva!')
    except subprocess.CalledProcessError:
        update.message.reply_text('La stazione è attualmente spenta.')
"""

def main():
    upd= Updater(TOKEN)
    disp=upd.dispatcher

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("start_detection", start_detection))
    disp.add_handler(CommandHandler("show_website", show_website))
    # disp.add_handler(CommandHandler("check_status", check_status))

    upd.start_polling()
    upd.idle()

if __name__=='__main__':
    main()
