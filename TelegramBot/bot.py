import json
from telegram import Update, Application
from telegram.ext import CommandHandler, ContextTypes
from asyncio import Queue

DEBUG = 1

def getToken():
    with open('conn/telegramBot.json', 'r') as json_file:
        data = json.load(json_file)
    token = data['token']
    return token

def __debug(msg):
    if DEBUG:
        print("\033[94m[DEBUG]\033[0m", msg)

# def start(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text('Hello! This is the start command.')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! This is the start command.')

def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    update.message.reply_text('Help!')

def main():
 def main():
    TOKEN = getToken()  # Ensure this retrieves your bot's token

    # Create the Application using the bot token
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.run_polling()

if __name__ == "__main__":
    main()
