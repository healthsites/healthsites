# -*- coding: utf-8 -*-
from optparse import make_option

import json

import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from localities.models import Locality
from localities.map_clustering import cluster
from localities.utils import parse_bbox, get_heathsites_master

class Command(BaseCommand):

    args = '<icon_width> <icon_height>'
    help = 'Generate locality cluster cache'

    option_list = BaseCommand.option_list + (
        make_option(
            '--tabs', action='store_true', dest='use_tabs', default=False,
            help='Use when input file is tab delimited'
        ),
    )

    def handle(self, *args, **options):

        if len(args) != 2:
            raise CommandError('Missing required arguments')

        try:
            icon_size = [int(size) for size in args[0:2]]
        except Exception as e:
            raise CommandError(str(e))

        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise CommandError('Icon sizes should be positive numbers')

        for zoom in range(settings.CLUSTER_CACHE_MAX_ZOOM + 1):
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                '{}_{}_{}_localities.json'.format(zoom, *icon_size)
            )

            localities = get_heathsites_master().in_bbox(parse_bbox('-180,-90,180,90'))
            object_list = cluster(localities, zoom, *icon_size)

            with open(filename, 'wb') as cache_file:
                json.dump(object_list, cache_file)

            self.stdout.write('Generated cluster cache for zoom: %s' % zoom)
