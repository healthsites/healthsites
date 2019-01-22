__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from django.http.response import HttpResponseBadRequest
from rest_framework import status
from rest_framework.response import Response

from localities.models import Locality
from localities.utils import parse_bbox
from localities_healthsites_osm.api_views.v2 import (
    ApiSchemaBase,
    PaginationAPI,
    Parameters,
)
from localities_osm.models.locality import LocalityOSMView


class ApiSchema(ApiSchemaBase):
    schemas = [
        Parameters.page, Parameters.extent,
        Parameters.output
    ]


class GetFacilities(PaginationAPI):
    """
    get:
    Returns a list of facilities with some filtering parameters.

    post:
    Create a facility.
    There are mandatory field for this:
    1. uuid : this is path parameters
    2. name
    3. lng & lat
    4. and some of required specification that will be show the error
    on the result (this specification is defined at admin site)

    5. Some attributes that has options. Can put other, but it will not be show
    on the healthsites map. This attributes should be array and can be more than one
    "activities": [
            "medicine and medical specialties",
            "surgery and surgical specialties",
            "Maternal and women health",
            "pediatric care"
        ],
    "ancillary_services": [
        "Operating theater",
        "laboratory",
        "imaging equipment",
        "intensive care unit"
    ],
    "scope_of_service": [
        "specialized care",
        "general acute care",
        "rehabilitation care",
        "old age/hospice care"
    ],

    6. Some attributes has it's own format
    "inpatient_service": {
        "full_time_beds": "3",
        "part_time_beds": "2"
    },
    "defining_hours": {
        "wed": [
            "09:00-17:00",
            "20:00-23:00",
        ],
        "sun": [],
        "fri": [],
        "tue": [],
        "mon": [],
        "thu": [],
        "sat": []
    },
    "staff": {
        "nurses": "1",
        "doctors": "3"
    }

    7. Some attributes is just 1 value but has options,
    will be error if not in these options.

    ownership : [
        public,
        private not for profit,
        private commercial]
    nature_of_facility : [
        clinic without beds,
        clinic with beds,
        first referral hospital,
        second referral hospital or General hospital,
        tertiary level including University hospital]
    """
    filter_backends = (ApiSchema,)

    def get(self, request):
        validation = self.validation()
        if validation:
            return HttpResponseBadRequest(validation)

        # check extent data
        queryset = LocalityOSMView.objects.all()
        extent = request.GET.get('extent', None)
        if extent:
            try:
                polygon = parse_bbox(request.GET.get('extent'))
                queryset = queryset.in_polygon(polygon)
            except (ValueError, IndexError):
                return HttpResponseBadRequest('extent is incorrect format')

        # TODO:Find a way how to get osm update time
        # # check by timestamp data
        # timestamp_from = request.GET.get('from', None)
        # if timestamp_from:
        #     try:
        #         queryset = queryset.from_datetime(
        #             datetime.fromtimestamp(int(timestamp_from))
        #         )
        #     except TypeError:
        #         return HttpResponseBadRequest('From needs to be in integer')
        # timestamp_to = request.GET.get('to', None)
        # if timestamp_to:
        #     try:
        #         queryset = queryset.to_datetime(
        #             datetime.fromtimestamp(int(timestamp_to))
        #         )
        #     except TypeError:
        #         return HttpResponseBadRequest('From needs to be in integer')

        queryset = self.get_query_by_page(queryset)
        return Response(self.serialize(queryset, many=True))

    def post(self, request):
        # TODO: Create also into osm database
        data = request.data
        facility = Locality()
        try:
            facility.update_data(data, request.user)
            return Response(self.serialize(facility), status=status.HTTP_201_CREATED)
        except KeyError as e:
            return HttpResponseBadRequest('%s is required' % e)
        except ValueError as e:
            return HttpResponseBadRequest('%s' % e)
