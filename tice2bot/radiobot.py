import logging

from telegram.ext import Updater

from config.bot_config import TOKEN
from api.common.loader import CommandsLoader

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=TOKEN)
    CommandsLoader().load(updater.dispatcher)
    updater.start_polling()

