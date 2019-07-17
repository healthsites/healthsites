__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/07/19'

from django.http import Http404, HttpResponseForbidden
from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from api.api_views.v2.base_api import BaseAPIWithAuth
from api.api_views.v2.pagination import PaginationAPI
from localities_osm_extension.models.pending_state import PendingReview
from localities_osm_extension.serializer.pending_state import (
    PendingReviewSerializer, PendingReviewGeoSerializer)


class GetDetailPendingReviews(BaseAPIWithAuth, PaginationAPI):
    """
    get:
    Returns detail of pending review

    """

    def get(self, request, id):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)

        try:
            data = PendingReview.objects.get(id=id)
            if data.uploader != request.user:
                return HttpResponseForbidden()
        except PendingReview.DoesNotExist:
            raise Http404()

        if self.format == 'json':
            return Response(PendingReviewSerializer(data).data)
        elif self.format == 'geojson':
            return Response(PendingReviewGeoSerializer(data).data)
        else:
            return HttpResponseBadRequest('%s is not recognized' % self.format)

    def delete(self, request, id):
        try:
            PendingReview.objects.get(id=id).delete()
            return Response('OK')
        except PendingReview.DoesNotExist:
            raise Http404()
