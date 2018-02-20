""" Common libraries """
import socket

import json

from urllib import request
from urllib.error import URLError


from config.bot_config import ICECAST2_SERVERS, ICECAST2_STATS_FILE, SERVERS_LIMIT, SSL, NGINX_SSL


class RadioStream:

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


class CheckIceCast2Stats:

    """CheckIceCast2Stats"""

    def __init__(self):

        self.servers = []

    def get_stats(self):

        """get_stats"""

        for srv in ICECAST2_SERVERS:

            try:
                srv_request = request.urlopen('{}/{}'.format(srv, ICECAST2_STATS_FILE), None, 3)

            except URLError:
                # no stream or server is down
                pass

            else:

                if srv_request.getcode() == 200:

                    stats_data = json.loads(srv_request.read().decode('utf-8'))

                    if 'icestats' in stats_data and 'source' in stats_data['icestats']:

                        # if the server limit reach SERVERS_LIMIT - 5, will not be listen as available
                        if stats_data['icestats']['source']['listeners'] >= SERVERS_LIMIT - 5:
                            continue

                        radio = RadioStream()

                        radio.stream = stats_data['icestats']['source']['listenurl']

                        if SSL is True and radio.stream.startswith('http:'):
                            radio.stream = radio.stream.replace('http', 'https')
                        
                        if NGINX_SSL is True and ':8000' in radio.stream:
                            radio.stream = radio.stream.replace(':8000', '')

                        radio.server = socket.gethostbyname(stats_data['icestats']['host'])
                        radio.online = stats_data['icestats']['source']['listeners']
                        self.servers.append(radio)

        return self.servers


class CommonCommands:

    def get_streams(self, bot, update):

        """
        get_streams

        :param bot
        :param update
        """

        ice_stats = CheckIceCast2Stats()
        stats = ice_stats.get_stats()

        if not stats:

            bot.sendMessage(chat_id=update.message.chat_id, text='There are no active streams')
            return False

        return stats

    def get_user_data(self, bot, update):

        """
        get_user_data

        :param bot
        :param update
        """

        user_data = bot.get_chat(update.message.chat_id)

        # if username does not exist, we cannot continue, so we just message back, how to create a username
        if not user_data.username:

            bot.sendMessage(
                chat_id=update.message.chat_id, text="Please set your username ( telegram -> settings)"
            )

            bot.sendMessage(
                chat_id=update.message.chat_id,
                text="More info @ https://telegram.org/faq#q-what-are-usernames-how-do-i-get-one"
            )

            bot.sendMessage(
                chat_id=update.message.chat_id, text="Note that, for this session was created a random username"
            )

            user_data.username = uuid.uuid4()

        return user_data

