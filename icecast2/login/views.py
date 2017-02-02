from urllib.parse import urlparse, parse_qs
from rest_framework.views import APIView
from rest_framework.response import Response

import redis

redis_ctx = redis.Redis(host='localhost', port=6379, db=0)

class IceCast2Login(APIView):

    """IceCast2Login"""

    def post(self, request):
        """
        post

        :param request
        """

        data = request.POST.get('mount')
        data = urlparse(data)
        data = parse_qs(data.query)

        password = redis_ctx.get(data.get('username')[0])

        result = Response()

        if password and password == data.get('password')[0].encode('utf-8'):
            result['icecast-auth-user'] = 1

        else:
            result['icecast-auth-user'] = 0

        return result

