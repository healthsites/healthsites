__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/07/19'

from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponseForbidden
from rest_framework.views import APIView, Response
from localities_osm_extension.models.pending_state import PendingState


class GetPending(APIView):
    """ Get pending states by user """

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

        if user != request.user:
            return HttpResponseForbidden()

        pendings = PendingState.objects.filter(
            uploader=user)

        output = []
        for pending in pendings:
            output.append({
                'osm_id': pending.extension.osm_id,
                'osm_type': pending.extension.osm_type,
                'uploader': pending.uploader.username,
                'time_uploaded': pending.time_uploaded,
                'osm_name': pending.name,
                'version': pending.version
            })
        return Response(output)
