__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/06/19'

from localities.models import Country
from localities_osm.models.locality import LocalityOSMView
from localities.utils import parse_bbox


def all_locality():
    return LocalityOSMView.objects.filter(osm_id__isnull=False)


def filter_locality(
        extent=None, country=None, timestamp_from=None, timestamp_to=None):
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
                polygons = country.polygon_geometry
                queryset = queryset.in_polygon(polygons)
        except Country.DoesNotExist:
            raise Exception('%s is not found or not a country.' % country)

    if timestamp_from:
        queryset = queryset.filter(changeset_timestamp__gte=timestamp_from)

    if timestamp_to:
        queryset = queryset.filter(changeset_timestamp__lte=timestamp_to)

    return queryset
