""" RadioBot API """

import logging
import random
import json
import uuid
from urllib import request

import redis

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from config.bot_config import ICECAST2_SERVERS, ICECAST2_STATS_FILE, SERVERS_LIMIT
from config.bot_config import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_SESSION_EXPIRE

from api.common import RadioStream, CheckIceCast2Stats, CommonCommands
from api.interfaces import CommandHandlerAPI


class RadioBot(CommandHandlerAPI):

    """ IceCast2 Radio Bot """

    def __init__(self):

        self.redis_ctx = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

        self.log = logging.getLogger(name='RadioBot')
        self.common = CommonCommands()

    def start_tcb(self, bot, update, args):

        """
        start_tcb - callback triggered on /start command

        :param bot: bot object comes from telegram API
        :param update: update object comes from telegram API
        :param args: our custom args

        """

        user_data = bot.get_chat(update.message.chat_id)

        bot.sendMessage(
            chat_id=update.message.chat_id, text="Hello {}, I'm HMSU Radio Bot.".format(user_data.username)
        )

        # keyboard = [[InlineKeyboardButton("Get radiokey", callback_data='1'), InlineKeyboardButton("Help", callback_data='2')]]

        # reply_markup = InlineKeyboardMarkup(keyboard)

        # update.message.reply_text('Please choose:', reply_markup=reply_markup)


        bot.sendMessage(chat_id=update.message.chat_id, text="Type /help for full list of commands")

    def help_tcb(self, bot, update, args):

        """
        help_tcb - callback triggered on /help ecommand

        :param bot: Comes from telegram API
        :param update: Comes from telegram API
        :param args: Custom args

        """

        bot.sendMessage(chat_id=update.message.chat_id, text="HMSU Radio Bot Help")
        bot.sendMessage(chat_id=update.message.chat_id, text="Type: /radiokey to get your personal radio access")

    def radiokey_tcb(self, bot, update, args):

        """
        radiokey_tcb - will generate temporary access for user

        :param bot
        :param update
        :param args

        """

        streams = self.common.get_streams(bot, update)

        if streams is False:
            return

        user_data = self.common.get_user_data(bot, update)

        stream = random.choice(streams)

        # check if the username is already  exist
        is_registered = self.redis_ctx.get(user_data.username)

        if is_registered:
            password = is_registered.decode('utf-8')

        else:

            password = uuid.uuid4()

            self.redis_ctx.hset(password, "username", user_data.username)
            # the ip address will be set from iceauth hook
            self.redis_ctx.hset(password, "ip", "none")
            self.redis_ctx.hset(password, "stream", stream.stream)
            self.redis_ctx.hset(password, "server", stream.server)

            self.redis_ctx.expire(password, REDIS_SESSION_EXPIRE)
            self.redis_ctx.setex(user_data.username, password, REDIS_SESSION_EXPIRE)

        self.log.info('User: {} requesting a radio access'.format(user_data.username))

        private_url = '{}?key={}'.format(stream.stream, password)

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Done. Copy/paste this link: {} into your player or browser to tune in.".format(private_url)
        )

        bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Keep this link in secret, it's personal for you and will be valid in the next {} hours".format(
                int(REDIS_SESSION_EXPIRE / 3600)
            )
        )

