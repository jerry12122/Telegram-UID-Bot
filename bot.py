import os
import logging
import subprocess
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext 
from telegram.ext.filters import Filters
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler 
from telegram.ext.messagehandler import MessageHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
load_dotenv()
text = '''
指令列表:
/user 獲得user id
/enable_port [port] 開port
/disable_port [port] 關port
'''
ENABLE_PORT,DISABLE_PORT, EXPECT_BUTTON_CLICK = range(2)
def ufw_control(port,isOpen):
    isDelete = "" if isOpen else "delete"
    cmd = f"ufw {isDelete} allow {port}"
    return subprocess.check_output(cmd, shell=True).decode("utf-8")

if os.getenv('TOKEN')!=None:
    try:
        updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    except:
        print("Invalid token exception")
        quit()

    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # 幫助
    def help(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    # 返回使用者ID
    def user(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.effective_chat.id)

    def set_port(update: Update, context: CallbackContext):
        if update.effective_chat.id == int(os.getenv('ADMIN_UID')):
            button = [[InlineKeyboardButton("enable", callback_data='enable'),InlineKeyboardButton("disable", callback_data='disable')]]
            markup = InlineKeyboardMarkup(button)
            update.message.reply_text('請選擇動作', reply_markup=markup)
            return EXPECT_BUTTON_CLICK
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="沒有權限")
            return ConversationHandler.END

    def button_click_handler(update: Update, context: CallbackContext):
        query = update.callback_query
        context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入port")
        if query.data == 'enable':
            return ENABLE_PORT
        elif query.data == 'disable':
            return DISABLE_PORT

    def enable_port_input(update: Update, context: CallbackContext):
        port = update.message.text
        try:
            direct_output = ufw_control(port,True)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{port}已開放\n{direct_output}')
            logging.info(f"{update.effective_chat.id}:{port} is Opened.")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="錯誤")
        return ConversationHandler.END

    def disable_port_input(update: Update, context: CallbackContext):
        port = update.message.text
        try:
            direct_output = ufw_control(port,False)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{port}已關閉\n{direct_output}')
            logging.info(f"{update.effective_chat.id}:{port} is Closed.")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="錯誤")
        return ConversationHandler.END

    def cancel(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Name Conversation cancelled by user.')
        return ConversationHandler.END

    help_handler = CommandHandler("help", help)
    user_handler = CommandHandler('user', user)
    port_handler = ConversationHandler(
        entry_points=[CommandHandler('port', set_port)],
        states={
            ENABLE_PORT: [MessageHandler(Filters.text, enable_port_input)],
            DISABLE_PORT: [MessageHandler(Filters.text, disable_port_input)],
            EXPECT_BUTTON_CLICK:[CallbackQueryHandler(button_click_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(user_handler)
    dispatcher.add_handler(port_handler)

    updater.start_polling()
else:
    print('env error')