
import os
import logging
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import MessageFilter
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext 

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
    def enable_ssh(update: Update, context: CallbackContext):
        if update.effective_chat.id == int(os.getenv('ADMIN_UID')):
            cmd = f"ufw allow {os.getenv('SSH_PORT')}"
            os.system(cmd)
            context.bot.send_message(chat_id=update.effective_chat.id, text="ssh port已開放")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="沒有權限")
    def disable_ssh(update: Update, context: CallbackContext):
        if update.effective_chat.id == int(os.getenv('ADMIN_UID')):
            cmd = f"ufw delete allow {os.getenv('SSH_PORT')}"
            os.system(cmd)
            context.bot.send_message(chat_id=update.effective_chat.id, text="ssh port已禁用")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="沒有權限")

    user_handler = CommandHandler('user', user)
    enable_ssh_handler = CommandHandler('enable_ssh', enable_ssh)
    disable_ssh_handler = CommandHandler('disable_ssh', disable_ssh)
    dispatcher.add_handler(user_handler)
    dispatcher.add_handler(enable_ssh_handler)
    dispatcher.add_handler(disable_ssh_handler)
    
    class helpFilter(MessageFilter):
        def filter(self, message):
            cmdList= ['/user','/enable_ssh','/disable_ssh']
            return message.text not in cmdList

    help_filter = helpFilter()

    def help(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text="輸入/user獲得user id")

    help_handler = MessageHandler(help_filter, help)
    dispatcher.add_handler(help_handler)

    updater.start_polling()
else:
    print('env error')