__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import Http404, HttpResponseBadRequest
from rest_framework.response import Response
from api.api_views.v2.facilities.base_api import (
    BaseAPI
)
from localities.models import Locality
from localities_healthsites_osm.models.locality_healthsites_osm import (
    LocalityHealthsitesOSM
)
from localities_osm.models.locality import (
    LocalityOSMView
)
from localities_healthsites_osm.serializer.locality import (
    LocalityHealthsitesOSMSerializer,
    LocalityHealthsitesOSMGeoSerializer
)


class GetDetailFacility(BaseAPI):
    """
    get:
    Returns a facility detail.
    """
    JSONSerializer = LocalityHealthsitesOSMSerializer
    GEOJSONSerializer = LocalityHealthsitesOSMGeoSerializer

    def get(self, request, uuid):
        try:
            facility = LocalityHealthsitesOSM.objects.get(
                healthsite__uuid=uuid)
            facility = LocalityOSMView.objects.get(
                osm_type=facility.osm_type,
                osm_id=facility.osm_id
            )
            return Response(self.serialize(facility))
        except (Locality.DoesNotExist, LocalityHealthsitesOSM.DoesNotExist, LocalityOSMView):
            raise Http404()
