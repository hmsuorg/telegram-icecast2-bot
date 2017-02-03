""" Config File """

# change this to your telegram token
TOKEN = '

# list of IceCast2 servers
ICECAST2_SERVERS = [
    'http://radio2.hmsu.org:42024',
    'http://radio3.hmsu.org:8000',
]

ICECAST2_STATS_FILE = 'status-json.xsl'
SERVERS_LIMIT = 100

########
# Redis

REDIS_HOST = 'localhost'
REDIS_POST = 6379
REDIS_DB = 0
SESSION_EXPIRE = 24 * 3600  # 24h

