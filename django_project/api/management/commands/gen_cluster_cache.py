# -*- coding: utf-8 -*-
import json
import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.utilities.clustering import oms_view_cluster
from api.utilities.geometry import parse_bbox
from localities.models import Country
from localities_osm.utilities import get_all_osm_query


class Command(BaseCommand):
    """ Command to generate cluster cache for each country
    so cluster request can be fast.

     This command will be put in cron job for every 1 hour """
    default_size = [48, 46]
    args = '<icon_width> <icon_height>'
    help = 'Generate healthsites cluster cache. \n' \
           'icon_width and icon_height are the size that is used to make clustering \n' \
           'the method : overlap healthsites (by the icon size) will be clustered)\n' \
           'default size for healthsite is %d,%d' % (default_size[0], default_size[1])

    option_list = BaseCommand.option_list + (
        make_option(
            '--tabs', action='store_true', dest='use_tabs', default=False,
            help='Use when input file is tab delimited'
        ),
    )

    def handle(self, *args, **options):

        if len(args) != 2:
            icon_size = self.default_size
        else:
            try:
                icon_size = [int(size) for size in args[0:2]]
            except Exception as e:
                raise CommandError(str(e))

        if any((size < 0 for size in icon_size)):
            # icon sizes should be positive
            raise CommandError('Icon sizes should be positive numbers')

        # check the folder
        if not os.path.exists(settings.CLUSTER_CACHE_DIR):
            os.makedirs(settings.CLUSTER_CACHE_DIR)

        osm_query = get_all_osm_query()
        for zoom in range(settings.CLUSTER_CACHE_MAX_ZOOM + 1):
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                '{}_{}_{}_localities.json'.format(zoom, *icon_size)
            )

            localities = osm_query.in_bbox(parse_bbox('-180,-90,180,90'))
            object_list = oms_view_cluster(localities, zoom, *icon_size)

            with open(filename, 'wb') as cache_file:
                json.dump(object_list, cache_file)

            self.stdout.write('Generated cluster cache for zoom: %s' % zoom)

        for country in Country.objects.all():
            self.stdout.write('Generated cluster for %s' % country.name)
            polygon = country.polygon_geometry
            localities = osm_query.in_polygon(polygon)
            for zoom in range(settings.CLUSTER_CACHE_MAX_ZOOM + 1):
                filename = os.path.join(
                    settings.CLUSTER_CACHE_DIR,
                    '{}_{}_{}_localities_{}.json'.format(
                        zoom, icon_size[0], icon_size[1], country.name.encode('utf-8')
                    )
                )

                object_list = oms_view_cluster(localities, zoom, *icon_size)

                with open(filename, 'wb') as cache_file:
                    json.dump(object_list, cache_file)

                self.stdout.write('Generated cluster cache for zoom: %s' % zoom)
