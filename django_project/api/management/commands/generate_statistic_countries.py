__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/06/19'

import os
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
        # create already run indicator
        dirname = os.path.dirname(filename)
        is_run_file = os.path.join(dirname, 'is_run')
        if os.path.exists(filename):
            if os.path.exists(is_run_file):
                print '%s statistic generation already run' % country
                LOG.info('%s statistic generation already run' % country)
                return
            try:
                file = open(is_run_file, 'w+')
                file.close()
            except IOError as e:
                pass

        cache_data = get_statistic_cache(extent, country)
        healthsites = filter_locality(
            extent=extent, country=country)

        if cache_data:
            if cache_data['localities'] == healthsites.count():
                LOG.info('%s statistic generated skipped' % country)
                os.remove(is_run_file)  # remove run indicator
                return

        statistic = get_statistic(healthsites)

        # save the process
        LOG.info('%s statistic generated' % country)
        try:
            file = open(filename, 'w+')
            file.write(json.dumps(statistic))
            file.close()
            os.remove(is_run_file)  # remove run indicator
        except IOError as e:
            pass
        except Exception as e:
            print e
