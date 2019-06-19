__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/06/19'

from localities.models import Country
from localities_osm.models.locality import LocalityOSMView
from localities.utils import parse_bbox


def all_locality():
    return LocalityOSMView.objects.filter(osm_id__isnull=False)


def filter_locality(extent=None, country=None):
    """ Filter osm locality by extent and country
    :param extent: extent of data
    :type extent: str (with comma separator)

    :param country: specific country
    :type country: str

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
                polygons = country.polygon_geometry
                queryset = queryset.in_polygon(polygons)
        except Country.DoesNotExist:
            raise Exception('%s is not found or not a country.' % country)
    return queryset
