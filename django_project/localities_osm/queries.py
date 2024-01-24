__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from django.contrib.gis.geos import Polygon
from api.api_views.v2.geocode.search import search_by_geoname
from core.utils import parse_bbox
from localities.models.administration import Country
from localities_osm.models.locality import LocalityOSMView


def all_locality():
    return LocalityOSMView.objects.filter(osm_id__isnull=False)


def filter_locality(
        extent=None, country=None, timestamp_from=None, timestamp_to=None, place=None, filters={}):
    """ Filter osm locality by extent and country
    :param extent: extent of data
    :type extent: str (with comma separator)

    :param country: specific country
    :type country: str

    :param timestamp_from: start time
    :type timestamp_from: timestamp

    :param timestamp_to: end time
    :type timestamp_to: timestamp

    :return: LocalityOSMView
    """
    # check extent data
    queryset = all_locality()
    if extent:
        try:
            polygon = parse_bbox(extent)
        except (ValueError, IndexError):
            raise Exception('extent is incorrect format')
        queryset = queryset.in_polygon(polygon)

    # check by country
    if country:
        try:
            # getting country's polygon
            country = Country.objects.get(
                name__iexact=country)
            if country:
                queryset = queryset.in_administrative(country.get_codes)
        except Country.DoesNotExist:
            raise Exception('%s is not found or not a country.' % country)

    if place:
        try:
            geo = search_by_geoname(place)
            bbox = (geo['southwest']['lng'], geo['southwest']['lat'],
                    geo['northeast']['lng'], geo['northeast']['lat'])
            geom = Polygon.from_bbox(bbox)
            queryset = queryset.filter(geometry__within=geom)
        except Exception:
            pass

    if timestamp_from:
        queryset = queryset.filter(changeset_timestamp__gte=timestamp_from)

    if timestamp_to:
        queryset = queryset.filter(changeset_timestamp__lte=timestamp_to)
    if filters:
        queryset = queryset.in_filters(filters)
    return queryset
