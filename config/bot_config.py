""" Config File """

TOKEN = 'YOUR_TELEGRAM_TOKEN'

ICECAST2_SERVERS = [
    'http://radio2.hmsu.org:42024',
    'http://radio3.hmsu.org:8000',
]

ICECAST2_STATS_FILE = 'status-json.xsl'

PROTECTED_STREAM_URL = '/hmsu-shano.ogg'

SERVERS_LIMIT = 100
TOTAL_USERS = SERVERS_LIMIT * len(ICECAST2_SERVERS)

SESSION_EXPIRE = 24 * 3600  # 24h

