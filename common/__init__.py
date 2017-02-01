# common functions
from telegram.ext import CommandHandler


def dispatch(bot, dispatcher):

    for callback in dir(bot):

        if callback.endswith('_tcb'):
            dispatcher.add_handler(CommandHandler(callback.replace('_tcb', ''), getattr(bot, callback), pass_args=True))


