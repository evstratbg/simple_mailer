from datetime import datetime as dt

from telegram import ReplyKeyboardRemove, ParseMode, Bot, Update
from telegram.ext import ConversationHandler, CommandHandler, \
    Filters, MessageHandler

from models import Chats, Messages
from bot_app.handlers.manage_chats import start

from config import ADMINS
from logger import log


@log
def ask_text(bot: Bot, update: Update):
    uid = update.message.from_user.id
    if uid not in ADMINS:
        return

    bot.send_message(
        uid,
        'Что будем рассылать?',
        reply_markup=ReplyKeyboardRemove(),
        disable_notification=True
    )
    return 2


@log
def start_mailing(bot: Bot, update: Update):
    uid = update.message.from_user.id
    message = update.message.text
    chats = Chats.select()
    for chat in chats:
        Messages.create(
            owner=uid, text=message, chat_id=chat.id, send_dt=dt.now()
        )
        bot.send_message(
            chat.id,
            message,
            parse_mode=ParseMode.HTML
        )
    bot.send_message(
        uid,
        'Рассылку закончил'
    )
    return ConversationHandler.END


def register(dp):
    start_admin = ConversationHandler(
        entry_points=[CommandHandler('mail', ask_text)],
        states={
            2: [
                MessageHandler(
                    Filters.all,
                    start_mailing
                )],
        },
        fallbacks=[CommandHandler('start', start)]
    )
    dp.add_handler(start_admin)
