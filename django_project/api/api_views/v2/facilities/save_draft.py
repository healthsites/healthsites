__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '06/04/20'

from django.http.response import HttpResponseServerError
from rest_framework.response import Response
from rest_framework.views import APIView
from api.utils import save_draft_data


class SaveDraft(APIView):
    def post(self, request):
        try:
            ids = request.data['ids'].split(',')
            save_draft_data(
                request.user, ids,
                request.data['comment'], request.data['source'])
            return Response('OK')
        except Exception as e:
            return HttpResponseServerError('%s' % e)
