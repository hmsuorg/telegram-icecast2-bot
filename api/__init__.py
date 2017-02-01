""" RadioBot API """

import random
import json
import uuid
from urllib import request
import redis

from config.bot_config import ICECAST2_SERVERS, SESSION_EXPIRE, ICECAST2_STATS_FILE, SERVERS_LIMIT


class CheckIceCast2Stats:

    """CheckIceCast2Stats"""

    def __init__(self):

        self.servers = []

    def get_stats(self):

        """get_stats"""

        for srv in ICECAST2_SERVERS:

            srv_request = request.urlopen('{}/{}'.format(srv, ICECAST2_STATS_FILE), None, 3)

            if srv_request.getcode() == 200:

                stats_data = json.loads(srv_request.read().decode('utf-8'))

                if 'icestats' in stats_data and 'source' in stats_data['icestats']:

                    # if the server limit reach SERVERS_LIMIT - 5, will not be listen as available
                    if stats_data['icestats']['source']['listeners'] >= SERVERS_LIMIT - 5:
                        continue

                    radio = RadioStreams()

                    radio.stream = stats_data['icestats']['source']['listenurl']
                    radio.server = srv
                    radio.online = stats_data['icestats']['source']['listeners']
                    self.servers.append(radio)

        return self.servers


class RadioStreams:

    """RadioStreams"""

    def __init__(self):

        """__init__"""

        self.__stream = None
        self.__server = None
        self.__online = 0

    @property
    def stream(self):
        """stream"""
        return self.__stream

    @stream.setter
    def stream(self, stream):
        """
        stream

        :param stream
        """
        self.__stream = stream

    @property
    def server(self):
        """server"""
        return self.__server

    @server.setter
    def server(self, host):

        """
        server

        :param host
        """
        self.__server = host

    @property
    def online(self):
        """online"""
        return self.__online

    @online.setter
    def online(self, online):
        self.__online = online

class RadioBot:

    """RadioBot"""

    def __init__(self):

        self.redis_ctx = redis.Redis(host='localhost', port=6379, db=0)

        self.stats = CheckIceCast2Stats()

    def start_tcb(self, bot, update, args):

        """
        start_tcb - callback triggered on /start command

        :param bot: bot object comes from telegram API
        :param update: update object comes from telegram API
        :param args: our custom args

        """

        bot.sendMessage(chat_id=update.message.chat_id, text="Hello I'm HMSU Radio Bot.")
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

        user_data = bot.get_chat(update.message.chat_id)

        # if user name is not set, we cannot continue, so we just message back, how to create a username
        if not user_data.username:

            bot.sendMessage(
                chat_id=update.message.chat_id, text="Please set your username ( telegram -> settings)"
            )

            bot.sendMessage(
                chat_id=update.message.chat_id, text="More info @ https://telegram.org/faq#q-what-are-usernames-how-do-i-get-one"
            )


            return

        # check if the username is already  exist
        is_register = self.redis_ctx.get(user_data.username)

        if is_register:
            password = is_register.decode('utf-8')

        else:

            password = uuid.uuid4()
            self.redis_ctx.setex(user_data.username, password, SESSION_EXPIRE)


        stats = self.stats.get_stats()

        if stats:

            stream = random.choice(stats)

            private_url = stream.stream.replace('//', '//{}:{}@'.format(user_data.username, password))

            bot.sendMessage(
                chat_id=update.message.chat_id,
                text="Done, your username is: {}, with password: {}, tune in @ {} or copy/paste this link: {} into your player or browser".format(
                    user_data.username, password, stream.server, private_url
                )
            )

        else:

            bot.sendMessage(chat_id=update.message.chat_id, text='There are no active streams')

