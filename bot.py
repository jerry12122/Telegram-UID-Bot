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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
"""
help - 獲得幫助
user - 獲得user id
port - 設定防火牆
frp - 設定frp
"""
load_dotenv()
text = os.getenv('HELP_MESSAGE')
ENABLE_PORT, DISABLE_PORT, GET_STATUS ,UFW_BUTTON_CLICK,FRP_BUTTON_CLICK = range(5)
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
    # /port後會執行得動作
    def set_port(update: Update, context: CallbackContext):
        if update.effective_chat.id == int(os.getenv('ADMIN_UID')):
            button = [[InlineKeyboardButton("enable", callback_data='enable'),InlineKeyboardButton("disable", callback_data='disable')]]
            markup = InlineKeyboardMarkup(button)
            update.message.reply_text('請選擇動作', reply_markup=markup)
            return UFW_BUTTON_CLICK
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="沒有權限")
            return ConversationHandler.END
    # 按下按鈕後會執行的動作
    def ufw_click_handler(update: Update, context: CallbackContext):
        query = update.callback_query
        context.bot.send_message(chat_id=update.effective_chat.id, text="請輸入port")
        if query.data == 'enable':
            return ENABLE_PORT
        elif query.data == 'disable':
            return DISABLE_PORT
    # 如果按下enable會執行的動作
    def enable_port_input(update: Update, context: CallbackContext):
        port = update.message.text
        try:
            direct_output = ufw_control(port,True)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{port}已開放\n{direct_output}')
            logging.info(f"{update.effective_chat.id}:{port} is Opened.")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="錯誤")
        return ConversationHandler.END
    # 如果按下disable會執行的動作
    def disable_port_input(update: Update, context: CallbackContext):
        port = update.message.text
        try:
            direct_output = ufw_control(port,False)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{port}已關閉\n{direct_output}')
            logging.info(f"{update.effective_chat.id}:{port} is Closed.")
        except:
            context.bot.send_message(chat_id=update.effective_chat.id, text="錯誤")
        return ConversationHandler.END
    # 取消動作
    def cancel(update: Update, context: CallbackContext):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Name Conversation cancelled by user.')
        return ConversationHandler.END
    # /frp後會執行的動作
    def frp_action(update: Update, context: CallbackContext):
        if update.effective_chat.id == int(os.getenv('ADMIN_UID')):
            button = [[InlineKeyboardButton("reload", callback_data='reload')]]
            markup = InlineKeyboardMarkup(button)
            update.message.reply_text('請選擇動作', reply_markup=markup)
            return FRP_BUTTON_CLICK
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="沒有權限")
            return ConversationHandler.END
    # 按下按鈕後會執行的動作
    def frp_click_handler(update: Update, context: CallbackContext):
        query = update.callback_query
        if query.data == 'reload':
            cmd = os.getenv('FRP_RELOAD_CMD')
            cmd_return = subprocess.check_output(cmd, shell=True).decode("utf-8")
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'{cmd_return}')
        else :
            context.bot.send_message(chat_id=update.effective_chat.id, text="錯誤")
        return ConversationHandler.END

    help_handler = CommandHandler("help", help)
    user_handler = CommandHandler('user', user)
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('port', set_port),CommandHandler('frp', frp_action)],
        states={
            ENABLE_PORT: [MessageHandler(Filters.text, enable_port_input)],
            DISABLE_PORT: [MessageHandler(Filters.text, disable_port_input)],
            UFW_BUTTON_CLICK:[CallbackQueryHandler(ufw_click_handler)],
            FRP_BUTTON_CLICK:[CallbackQueryHandler(frp_click_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(user_handler)
    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
else:
    print('env error')