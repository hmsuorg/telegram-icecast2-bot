from urllib.parse import parse_qs
from japronto import Application

import redis

redis_ctx = redis.Redis(host='localhost', port=6379, db=0)


def IceCast2Login(request):

    auth = {}

    _, data = request.form['mount'].split('?')
    data = parse_qs(data)

    password = redis_ctx.get(data.get('username')[0])

    if password and password == data.get('password')[0].encode('utf-8'):
        auth['icecast-auth-user'] = '1'

    else:
        auth['icecast-auth-user'] = '0'

    return request.Response(text='', headers=auth)


app = Application()
app.router.add_route('/icecast/', IceCast2Login, methods=['POST'])
app.run(host="192.168.10.109", port=8000)
