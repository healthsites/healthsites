__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/06/19'

import json
import logging
import os
from django.conf import settings
from django.db.models import Count
from localities.tasks import country_data_into_statistic_task
from localities_osm.queries import filter_locality
from localities_osm.models.locality import LocalityOSM
from localities_osm.serializer.locality_osm import LocalityOSMBasicSerializer

LOG = logging.getLogger(__name__)


def get_statistic_cache_filename(extent=None, country=None):
    """ Get statistic cache filename of localities by extent and country
    :param extent: extent of data
    :type extent: str (with comma separator)

    :param country: specific country
    :type country: str

    :return: json
    """
    country_name = 'world'
    if country:
        country_name = country.lower()

    dir_cache = os.path.join(
        settings.CACHE_DIR,
        'statistic',
        country_name)

    if not os.path.exists(dir_cache):
        os.makedirs(dir_cache)

    filename = os.path.join(
        dir_cache, 'statistic.json')
    if extent:
        filename = os.path.join(
            dir_cache, '%s.json' % extent)
    return filename


def get_statistic_cache(extent, country):
    """ Get cache statistic data.

    :param extent: extent of data
    :type extent: str (with comma separator)

    :param country: specific country
    :type country: str

    :return: json
    """
    try:
        cached_locs = open(get_statistic_cache_filename(
            extent, country), 'rb')
        cached_data = json.loads(cached_locs.read())
        return cached_data
    except (IOError, ValueError, KeyError) as e:  # noqa
        return None


def get_statistic_with_cache(extent, country, timestamp_from, timestamp_to):
    """ Checking cache of statistic data
    How it is work? Get cache, if it presents, return cache
    If not, call statistic function and save into cache.

    :param extent: extent of data
    :type extent: str (with comma separator)

    :param country: specific country
    :type country: str

    :return: json
    """
    cached_data = get_statistic_cache(extent, country)
    country_data_into_statistic_task.delay(extent, country)

    # if cahed data presented
    if cached_data:
        return cached_data

    # if not return from statistic
    return get_statistic(
        filter_locality(
            extent=extent,
            country=country,
            timestamp_from=timestamp_from,
            timestamp_to=timestamp_to
        )
    )


def get_statistic(healthsites):
    """ Get statistic of localities
    :return: json
    """
    statistic = {
        'localities': healthsites.count(),
        'numbers': {},
        'last_update': []
    }
    numbers = healthsites.values(
        'amenity').annotate(total=Count('amenity')).order_by('-total')
    for number in numbers[:5]:
        type = number['amenity']
        if type:
            statistic['numbers'][type] = number['total']

    # get completeness
    basic = LocalityOSM.get_count_of_basic(healthsites)
    complete = LocalityOSM.get_count_of_complete(healthsites)
    statistic['completeness'] = {
        'basic': basic,
        'complete': complete
    }

    # last update
    healthsites = healthsites.exclude(
        changeset_timestamp__isnull=True).order_by(
        '-changeset_timestamp')[:20]
    statistic['last_update'] = LocalityOSMBasicSerializer(
        healthsites, many=True).data
    return statistic
