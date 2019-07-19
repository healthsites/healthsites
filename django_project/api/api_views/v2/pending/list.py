__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/07/19'

from django.http.response import HttpResponseBadRequest
from rest_framework.response import Response
from api.api_views.v2.pagination import LessThanOneException, NotANumberException
from api.api_views.v2.base_api import BaseAPIWithAuth
from api.api_views.v2.pagination import PaginationAPI
from localities_osm_extension.models.pending_state import (
    PendingReview, PendingUpdate)
from localities_osm_extension.serializer.pending_state import (
    PendingReviewSerializer, PendingUpdateSerializer)


class GetPendingReviews(BaseAPIWithAuth, PaginationAPI):
    """
    get:
    Returns list of user data that is in review. This list is about the data that
    uploaded by user but was not success with a reason

    """

    def get(self, request, username):
        page = self.request.GET.get('page', None)
        if page:
            try:
                queryset = self.get_query_by_page(
                    PendingReview.objects.filter(uploader__username=username))
            except (LessThanOneException, NotANumberException) as e:
                return HttpResponseBadRequest('%s' % e)
        else:
            queryset = PendingReview.objects.filter(uploader__username=username)

        return Response(PendingReviewSerializer(queryset, many=True).data)


class GetPendingUpdates(BaseAPIWithAuth, PaginationAPI):
    """
    get:
    Returns list of user data that is in pending state. Pending update in here is the data
    that success uploaded into osm but still not pulled by docker osm cache
    """

    def get(self, request, username):
        page = self.request.GET.get('page', None)
        if page:
            try:
                queryset = self.get_query_by_page(
                    PendingUpdate.objects.filter(uploader__username=username))
            except (LessThanOneException, NotANumberException) as e:
                return HttpResponseBadRequest('%s' % e)
        else:
            queryset = PendingUpdate.objects.filter(uploader__username=username)

        return Response(PendingUpdateSerializer(queryset, many=True).data)
