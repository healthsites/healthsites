# -*- coding: utf-8 -*-
from api.views.api_view import ApiView
from localities.utils import get_heathsites_master, parse_bbox


class FacilitiesApiView(ApiView):
    """ An API view class for retrieving facilities

    It retruns facilties regarding parameter :
    - extent : by geometry
    - page : returns 100 facilities for each of page
    """

    def get(self, request, *args, **kwargs):
        validation = self.extract_request(request)
        if validation:
            return self.api_response(
                {'error': validation}
            )

        # get data
        if 'extent' in request.GET:
            polygon = parse_bbox(request.GET.get('extent'))

            # if page is not presented, use page = 1
            page = self.page
            if not page:
                page = 1

            facilities = self.get_query_by_page(
                get_heathsites_master().in_polygon(polygon), page
            )
            facilities = self.query_to_json(facilities, self.format)
            return self.api_response(facilities)

        elif 'page' in request.GET:
            if not self.page:
                return self.api_response(
                    {'error': "page is wrong type"}
                )
            facilities = self.get_query_by_page(get_heathsites_master(), self.page)
            facilities = self.query_to_json(facilities, self.format)
            return self.api_response(facilities)
        else:
            return self.api_response(
                {'error': "need parameter"}
            )
