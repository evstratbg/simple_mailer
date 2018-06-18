from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters

from logger import log
from models import Chats


@log
def get_and_save_chat(bot: Bot, update: Update):
    if update.message.new_chat_member == bot.get_me():
        chat_id = update.effective_chat.id
        Chats.create(id=chat_id)


@log
def delete_chat(bot: Bot, update: Update):
    if update.message.left_chat_member == bot.get_me():
        chat_id = update.effective_chat.id
        c = Chats.get(Chats.id == chat_id)
        c.delete_instance()


def register(dp: Dispatcher):
    dp.add_handler(
        MessageHandler(Filters.status_update.new_chat_members, get_and_save_chat)
    )
    dp.add_handler(
        MessageHandler(Filters.status_update.left_chat_member, delete_chat)
    )
