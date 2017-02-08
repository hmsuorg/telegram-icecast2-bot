from urllib.parse import parse_qs
from urllib.parse import urlparse

import tornado.ioloop
import tornado.web
import tornado.escape

import redis
from config.bot_config import REDIS_DB, REDIS_HOST, REDIS_PORT, WEBHOOK_IP, WEBHOOK_PORT

redis_ctx = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class MainHandler(tornado.web.RequestHandler):
    
    def post(self):
        
        data = urlparse(self.request.body_arguments['mount'][0])
        key = parse_qs(data.query).get(b'key')[0]

        test = redis_ctx.get(key)

        if test:
            print('{} is authenticated and starting listening'.format(test))
            self.set_header('icecast-auth-user', '1')
        
        else:
            self.set_header('icecast-auth-user', '0')


def make_app():
    
    return tornado.web.Application([
        (r"/icecast/", MainHandler),
    ])

if __name__ == "__main__":
    
    app = make_app()
    app.listen(8044)
    tornado.ioloop.IOLoop.current().start()

