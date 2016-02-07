# -*- coding: utf-8 -*-
from optparse import make_option

import json

import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from localities.models import Locality

from localities.utils import parse_bbox

from localities.map_clustering import cluster


class Command(BaseCommand):

    args = '<max_zoom> <icon_size>'
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
            max_zoom = int(args[0])
            icon_size = [int(size) for size in args[1].split(',')]
        except Exception as e:
            raise CommandError(str(e))

        if max_zoom < 0 or max_zoom > 7:
            raise CommandError('Max zoom should be between 0 and 6')
        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise CommandError('Icon sizes should be positive numbers')
        if len(icon_size) != 2:
            raise CommandError('Icon size a comma delimited height,width')

        for zoom in range(max_zoom):
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                '{}_{}_{}_localities.json'.format(zoom, *icon_size)
            )

            localities = Locality.objects.in_bbox(parse_bbox('-180,-90,180,90'))
            object_list = cluster(localities, zoom, *icon_size)

            with open(filename, 'wb') as cache_file:
                json.dump(object_list, cache_file)

            self.stdout.write('Generated cluster cache for zoom: %s' % zoom)
