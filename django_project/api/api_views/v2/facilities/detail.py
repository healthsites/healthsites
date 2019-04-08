__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import Http404, HttpResponseBadRequest
from rest_framework.response import Response
from api.api_views.v2.facilities.base_api import (
    BaseAPI
)
from api.serializer.locality_post import LocalityPostSerializer
from localities.models import Locality
from localities_healthsites_osm.models.locality_healthsites_osm import (
    LocalityHealthsitesOSM
)


class GetDetailFacility(BaseAPI):
    """
    get:
    Returns a facility detail.

    put:
    Update a facility.
    """

    def get(self, request, uuid):
        try:

            facility = Locality.objects.get(uuid=uuid)
            locality_osm, created = LocalityHealthsitesOSM.objects.get_or_create(
                healthsite=facility)
            facility = locality_osm.return_osm_view()
            return Response(self.serialize(facility))
        except Locality.DoesNotExist:
            raise Http404()

    def put(self, request, uuid):
        try:
            data = request.data
            data = self.parse_data(data)
            facility = Locality.objects.get(uuid=uuid)
            facility.update_data(data, request.user)
            return Response('OK')
        except KeyError as e:
            return HttpResponseBadRequest('%s is required' % e)
        except ValueError as e:
            return HttpResponseBadRequest('%s' % e)
        except TypeError as e:
            return HttpResponseBadRequest('%s' % e)
        except Locality.DoesNotExist:
            raise Http404()

    def delete(self, request, uuid):
        try:
            facility = Locality.objects.get(uuid=uuid)
            facility.delete()
            return Response('OK')
        except Locality.DoesNotExist:
            raise Http404()


class GetDetailFacilityPublic(BaseAPI):
    """
    get:
    Returns a facility detail.

    put:
    Update a facility.
    """

    def get_serializer(self):
        return LocalityPostSerializer()

    def get(self, request, uuid):
        try:

            facility = Locality.objects.get(uuid=uuid)
            locality_osm, created = LocalityHealthsitesOSM.objects.get_or_create(
                healthsite=facility)
            facility = locality_osm.return_osm_view()
            return Response(self.serialize(facility))
        except Locality.DoesNotExist:
            raise Http404()
