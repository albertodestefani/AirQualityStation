import json
import logging
from queue import Queue
from telegram.ext import Updater, CommandHandler, MessageHandler, Filter

# Imposta il livello di log
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def getToken():
    with open('../conn/telegramBot.json', 'r') as json_file:
        data = json.load(json_file)
    token = data['token']
    return token

# Definisci una funzione per gestire il comando /start
def start(update):
    update.message.reply_text('Benvenuto! Usa /start_detection per avviare la rilevazione e /show_website per vedere i risultati.')

# Definisci una funzione per gestire i messaggi di testo
def echo(update):
    update.message.reply_text(update.message.text)

def main():
    # Inserisci il tuo token del bot Telegram qui
    token = getToken()
    update_queue = Queue()  # Crea una coda
    updater = Updater(token, update_queue)
    
    # Ottieni il dispatcher per registrare i gestori di comandi e messaggi
    dispatcher = updater.dispatcher

    # Registra il gestore per il comando /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Registra il gestore per i messaggi di testo
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Avvia il bot
    updater.start_polling()

    # Mantieni il bot in esecuzione fino a quando non viene interrotto manualmente
    updater.idle()

if __name__ == '__main__':
    main()
