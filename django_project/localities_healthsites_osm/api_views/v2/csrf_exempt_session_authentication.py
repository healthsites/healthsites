__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '18/01/18'

from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening
