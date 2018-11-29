__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import Http404
from rest_framework.response import Response
from api.api_views.v2.schema import (
    ApiSchemaBase,
    Parameters
)
from api.api_views.v2.facilities.base_api import (
    BaseAPI
)
from localities.models import Locality


class ApiSchema(ApiSchemaBase):
    schemas = [
        Parameters.page, Parameters.extent,
        Parameters.timestamp_from, Parameters.timestamp_to,
        Parameters.output
    ]


class GetDetailFacility(BaseAPI):
    """
    Returns a facility detail.
    """
    filter_backends = (ApiSchema,)

    def get(self, request, uuid):
        try:
            facility = Locality.objects.get(uuid=uuid)
            return Response(self.serialize(facility))
        except Locality.DoesNotExist:
            raise Http404()
