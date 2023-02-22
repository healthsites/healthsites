# coding=utf-8
from rest_framework.views import APIView, Response


class ApiVersion1(APIView):

    def get(self, request):
        return Response(
            'This API is deprecated, please upgrade your application to use v3 '
            'of the API and register for your API token at URL'
        )


class ApiVersion2(APIView):

    def get(self, request):
        return Response(
            'This API is deprecated, please upgrade your application to use v3 '
            'of the API and register for your API token at URL'
        )
