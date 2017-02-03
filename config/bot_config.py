""" Config File """

####################################
# TELEGRAM
####################################

# Change this to your telegram token
TOKEN = ''


###################################
# ICECAST@
###################################

# List of IceCast2 servers

ICECAST2_SERVERS = [
    'http://radio2.hmsu.org:42024',
    'http://radio3.hmsu.org:8000',
]

ICECAST2_STATS_FILE = 'status-json.xsl'
SERVERS_LIMIT = 100

###################################
# Redis settings
###################################

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
SESSION_EXPIRE = 24 * 3600  # 24h

###################################
# WEB AUTH HOOK
###################################

WEBHOOK_IP = "192.168.10.109"
WEBHOOK_PORT = 8000
