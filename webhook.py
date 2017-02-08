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
            key = parse_qs(data.query).get(b'key')[0]

            ip = urlparse(self.request.body_arguments['ip'][0])
            ip = ip.path

            x_real_ip = self.request.headers.get("X-Real-IP")
            remote_ip = x_real_ip or self.request.remote_ip

            server_ip = redis_ctx.hget(key, "server")

            # if the user trying to play between the stream servers
            if server_ip != remote_ip:
                self.set_header('icecast-auth-user', '0')
                return

            username = redis_ctx.hget(key, "username")
            ip_redis = redis_ctx.hget(key, "ip")
            stream = redis_ctx.hget(key, "stream")

            if username:

                if ip_redis == b"none":
                    redis_ctx.hset(key, "ip", ip)
                    ip_redis = ip

                # if ip_redis is real ip but differ from the user's one
                # we have to reject this connection. The user need to renew his key

                if ip_redis and ip_redis != "none" and ip_redis != ip:
                    self.set_header('icecast-auth-user', '0')
                    return

                # if the stream name is different we have to rejecting this connections

                print('{} is authenticated and starting listening'.format(username))
                self.set_header('icecast-auth-user', '1')

            else:
                self.set_header('icecast-auth-user', '0')

        except Exception as e:

            print(e)
            self.set_header('icecast-auth-user', '0')


def make_app():

    return tornado.web.Application([
        (r"/icecast/", MainHandler),
    ])

if __name__ == "__main__":

    app = make_app()
    app.listen(8044)
    tornado.ioloop.IOLoop.current().start()

