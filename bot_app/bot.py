import logging

from telegram.ext import Updater

from bot_app.handlers import manage_chats, mailing


def run(logger_level, bot):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logger_level
    )

    updater = Updater(bot=bot)
    dp = updater.dispatcher

    manage_chats.register(dp)
    mailing.register(dp)

    updater.start_polling()
    updater.idle()
