""" Config File """

####################################
# TELEGRAM
####################################

# Change this to your telegram token
TOKEN = '315884542:AAF3bq1Wtz2nUlziF0Aic-oIgDvLM2xlnmE'

# List of bot owners

BOT_OWNERS = [
    'TargoliniHakini'  # telegram username
]

###################################
# ICECAST2
###################################

# List of your IceCast2 servers.

ICECAST2_SERVERS = [
    'https://radio2.hmsu.org:8000',
    'https://radio3.hmsu.org:8000',
]

# IceCast2 status files, depenends on IceCast2 config file.
# this web resource is public by default, so we used it to fetch
# statistics about the icecast2 server

ICECAST2_STATS_FILE = 'status-json.xsl'

# How many radio links can I serve?

SERVERS_LIMIT = 100

# icecast authentication web hooK
# this web hook is used by icecast2 url settings and specialy from listener_add
# more info @ https://icecast.org/docs/icecast-2.4.0/auth.html

WEBHOOK_IP = "192.168.10.109"
WEBHOOK_PORT = 8000

###################################
# Redis settings
###################################

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_SESSION_EXPIRE = 8 * 3600

