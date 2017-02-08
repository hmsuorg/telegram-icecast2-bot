from urllib.parse import parse_qs
from urllib.parse import urlparse

import tornado.ioloop
import tornado.web
import tornado.escape

import redis
from config.bot_config import REDIS_DB, REDIS_HOST, REDIS_PORT, WEBHOOK_IP, WEBHOOK_PORT, REDIS_SESSION_EXPIRE

redis_ctx = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class MainHandler(tornado.web.RequestHandler):

    def post(self):

        try:

            data = urlparse(self.request.body_arguments['mount'][0])

            ip = urlparse(self.request.body_arguments['ip'][0])
            ip = ip.path

            key = parse_qs(data.query).get(b'key')[0]

            username = redis_ctx.hget(key, "username")
            ip = redis_ctx.hget(key, "ip")
            stream = redis_ctx.hget(key, "stream")

            if username:

                redis_ctx.set(username, ip)

                print('{} is authenticated and starting listening'.format(username))
                self.set_header('icecast-auth-user', '1')

            else:
                self.set_header('icecast-auth-user', '0')

        except Exception as e:
            print(e)


def make_app():

    return tornado.web.Application([
        (r"/icecast/", MainHandler),
    ])

if __name__ == "__main__":

    app = make_app()
    app.listen(8044)
    tornado.ioloop.IOLoop.current().start()

