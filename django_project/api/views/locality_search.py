# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from api.views.api_view import ApiView
from frontend.views import search_place
from localities.models import Country, Locality, Value
from localities.utils import parse_bbox, get_heathsites_master


class LocalitySearchApiView(ApiView):
    """
    An API view class for retrieving facilities by search
    search it by place name of by facility name
    """

    def get_healthsite_master_by_polygon(self, polygon, facility_type):
        """ Get healthsites master by polygon.
        :return: filtered facilities
        """
        if facility_type:
            facilities_id = Value.objects. \
                filter(specification__attribute__key='type'). \
                filter(data=facility_type). \
                values_list('locality__id', flat=True)
            facilities = get_heathsites_master().filter(
                id__in=facilities_id).in_polygon(polygon)
        else:
            facilities = get_heathsites_master().in_polygon(polygon)

        if self.page:
            facilities = self.get_query_by_page(facilities, self.page)
        return facilities

    def get(self, request, *args, **kwargs):
        validation = self.extract_request(request)
        if validation:
            return self.api_response(
                {'error': validation}
            )

        if not 'name' in request.GET or not 'search_type' in request.GET:
            return self.api_response(
                {'error': "parameter is not enough"}
            )

        place_name = request.GET['name']
        search_type = request.GET['search_type']

        if search_type == "placename":
            try:
                countries = Country.objects.filter(
                    name__icontains=place_name
                )
                if len(countries) == 0:
                    raise Country.DoesNotExist
                country = None
                for country_query in countries:
                    if not country:
                        country = country_query
                    else:
                        if len(country.name) > len(country_query.name):
                            country = country_query
                polygon = country.polygon_geometry
            except Country.DoesNotExist:
                # if country is not found
                output = search_place(request, place_name)
                output['countries'] = ""
                bbox = output["southwest_lng"] + "," + \
                       output["southwest_lat"] + "," + \
                       output["northeast_lng"] + "," + \
                       output["northeast_lat"]
                try:
                    polygon = parse_bbox(bbox)
                except ValueError:
                    return self.api_response(
                        {'error': "place is not found"}
                    )

            facility_type = ""
            if 'facility_type' in request.GET:
                facility_type = request.GET['facility_type']

            facilities = self.get_healthsite_master_by_polygon(polygon, facility_type)
            facilities = self.query_to_json(facilities, self.format)
            return self.api_response(facilities)

        elif search_type == "facility":
            facilities = Locality.objects.filter(name__icontains=place_name)
            facilities = self.query_to_json(facilities, self.format)
            return self.api_response(facilities)
        else:
            return self.api_response(
                {'error': "search type is wrong"}
            )
