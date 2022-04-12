from telegram.ext import Updater
import logging

from telegram import Update
from telegram.ext import CallbackContext 
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

import os
from dotenv import load_dotenv

load_dotenv()
if os.getenv('TOKEN')!=None:
    try:
        updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    except:
        print("Invalid token exception")
        quit()
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    def user(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)
    
    user_handler = CommandHandler('user', user)
    dispatcher.add_handler(user_handler)
    from telegram.ext import MessageFilter

    class helpFilter(MessageFilter):
        def filter(self, message):
            return message.text != '/user'

    help_filter = helpFilter()

    def help(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="輸入/user獲得user id")

    help_handler = MessageHandler(help_filter, help)
    dispatcher.add_handler(help_handler)

    updater.start_polling()
else:
    print('env error')