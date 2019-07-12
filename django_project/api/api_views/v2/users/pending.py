__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/07/19'

from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponseForbidden
from rest_framework.views import APIView, Response
from api.utilities.pending import validate_pending_update
from localities_osm_extension.models.pending_state import PendingUpdate, \
    PendingReview


class GetPending(APIView):
    """ Get pending states by user """

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

        if user != request.user:
            return HttpResponseForbidden()

        pending_updates = PendingUpdate.objects.filter(uploader=user)
        pending_updates_output = []
        for pending_update in pending_updates:
            if validate_pending_update(
                    pending_update.extension.osm_type,
                    pending_update.extension.osm_id):
                pending_updates_output.append({
                    'osm_id': pending_update.extension.osm_id,
                    'osm_type': pending_update.extension.osm_type,
                    'uploader': pending_update.uploader.username,
                    'time_uploaded': pending_update.time_uploaded,
                    'osm_name': pending_update.name,
                    'version': pending_update.version
                })

        pending_reviews = PendingReview.objects.filter(uploader=user)
        pending_reviews_output = []
        for pending_review in pending_reviews:
            pending_reviews_output.append({
                'uploader': pending_review.uploader.username,
                'osm_name': pending_review.name,
                'reason': pending_review.reason,
                'payload': pending_review.payload,
                'time_uploaded': pending_review.time_uploaded,
            })

        response = {
            'pending_update': pending_updates_output,
            'pending_review': pending_reviews_output
        }

        return Response(response)
