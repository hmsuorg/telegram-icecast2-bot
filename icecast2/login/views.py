from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response


class IceCast2Login(APIView):

    def post(self, request, format=None):
        return Response({"success": True})
