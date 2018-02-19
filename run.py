import logging

from telegram import Bot
from telegram.ext import messagequeue as mq
from config import LOGGING_LEVELS, TOKENS
from argparse import ArgumentParser

from bot_app import run


def parse_argv():
    parser = ArgumentParser(description="Starts Mailer")
    parser.add_argument(
        '--token', '-t',
        type=str,
        default='TEST',
        help="api token name (from config) for access to bot")
    return parser.parse_args()


class MQBot(Bot):
    def __init__(self, *args, is_queued_def=True, mqueue=None, **kwargs):
        super(MQBot, self).__init__(*args, **kwargs)
        self._is_messages_queued_default = is_queued_def
        self._msg_queue = mqueue or mq.MessageQueue()

    def __del__(self):
        try:
            self._msg_queue.stop()
        except:
            pass
        super(MQBot, self).__del__()

    @mq.queuedmessage
    def send_message(self, *args, **kwargs):
        super(MQBot, self).send_message(*args, **kwargs)


if __name__ == '__main__':
    args = parse_argv()
    token_type = args.token.upper()
    token = TOKENS.get(token_type, TOKENS['TEST'])
    logger_level = LOGGING_LEVELS.get(token_type, logging.INFO)

    q = mq.MessageQueue()
    mqbot = MQBot(token, mqueue=q)

    startup_params = {
        'logger_level': logger_level,
        'bot': mqbot
    }

    run(**startup_params)
