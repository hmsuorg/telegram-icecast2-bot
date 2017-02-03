from urllib.parse import parse_qs
from japronto import Application

import redis

from config.bot_config import REDIS_DB, REDIS_HOST, REDIS_PORT, WEBHOOK_IP, WEBHOOK_PORT


class IceCast2Auth:

    def __init__(self):
        self.redis_ctx = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    def auth(self, request):

        auth = {}

        _, data = request.form['mount'].split('?')
        data = parse_qs(data)

        password = self.redis_ctx.get(data.get('username')[0])

        if password and password == data.get('password')[0].encode('utf-8'):
            auth['icecast-auth-user'] = '1'

        else:
            auth['icecast-auth-user'] = '0'

        return request.Response(text='', headers=auth)


app = Application()
app_auth = IceCast2Auth()

app.router.add_route('/icecast/', app_auth.auth, methods=['POST'])
app.run(host=WEBHOOK_IP, port=WEBHOOK_PORT)
