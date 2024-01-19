# coding=utf-8
from django.urls import reverse
from rest_framework.views import APIView, Response


class ApiVersion2(APIView):

    @property
    def error_text(self):
        url = reverse('enrollment-form')
        return (
            'This API is deprecated, '
            'please upgrade your application to use v3 '
            'of the API and register for your API token at this URL '
            f"{self.request.build_absolute_uri('/')[:-1]}{url}"
        )

    def get(self, request):
        return Response(self.error_text)
