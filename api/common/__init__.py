""" Common libraries """

import json

from urllib import request
from urllib.error import URLError


from config.bot_config import ICECAST2_SERVERS, ICECAST2_STATS_FILE, SERVERS_LIMIT


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

                        if radio.stream.startswith('http:'):
                            radio.stream.replace('http', 'https')
                            
                        radio.server = srv
                        radio.online = stats_data['icestats']['source']['listeners']
                        self.servers.append(radio)

        return self.servers

