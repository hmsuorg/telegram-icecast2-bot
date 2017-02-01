import logging

from telegram.ext import Updater

from config.bot_config import TOKEN
from api import RadioBot
from common import dispatch

if __name__ == "__main__":

    bot = RadioBot()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN)
    dispatch(bot, updater.dispatcher)
    updater.start_polling()

