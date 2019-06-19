__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/06/19'

import logging
import json
from django.core.management.base import BaseCommand
from api.utilities.statistic import (
    get_statistic,
    get_statistic_cache,
    get_statistic_cache_filename
)
from localities_osm.queries import filter_locality

LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        'This script to generate statistic cache.')

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--extent',
            dest='extent',
            help='extent in comma separator. Example : 0.4,-0.6,0.5,-0.4',
        )
        parser.add_argument(
            '--country',
            dest='country',
            help='Country name',
        )

    def handle(self, *args, **options):
        """ Do your work here """
        extent = options.get('extent', None)
        country = options.get('country', None)
        filename = get_statistic_cache_filename(
            extent=extent, country=country
        )
        cache_data = get_statistic_cache(extent, country)
        healthsites = filter_locality(
            extent=extent, country=country)

        if cache_data:
            if cache_data['localities'] == healthsites.count():
                LOG.info('%s statistic generated skipped' % country)
                return

        statistic = get_statistic(healthsites)

        # save the process
        LOG.info('%s statistic generated' % country)
        try:
            file = open(filename, 'w+')
            file.write(json.dumps(statistic))
            file.close()
        except Exception as e:
            pass
