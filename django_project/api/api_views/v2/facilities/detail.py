__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import Http404, HttpResponseBadRequest
from rest_framework.response import Response
from api.api_views.v2.facilities.base_api import (
    FacilitiesBaseAPI
)
from localities_osm.models.locality import LocalityOSMView


class GetDetailFacility(FacilitiesBaseAPI):
    """
    get:
    Returns a facility detail.

    put:
    Update a facility.
    """

    def get(self, request, osm_type, osm_id):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)
        try:

            facility = LocalityOSMView.objects.get(
                osm_type=osm_type,
                osm_id=osm_id)
            return Response(self.serialize(facility))
        except LocalityOSMView.DoesNotExist:
            raise Http404()
