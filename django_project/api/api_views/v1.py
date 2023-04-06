# coding=utf-8
from rest_framework.views import APIView, Response
from django.urls import reverse


class ApiVersion2(APIView):

    @property
    def error_text(self):
        url = reverse('enrollment-form')
        return (
            'This API is deprecated, '
            'please upgrade your application to use v3 '
            f"of the API and register for your API token at URL "
            f"{self.request.build_absolute_uri('/')[:-1]}{url}"
        )

    def get(self, request):
        return Response(self.error_text)
