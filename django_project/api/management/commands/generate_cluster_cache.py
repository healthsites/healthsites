# -*- coding: utf-8 -*-
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from api.utilities.clustering import oms_view_cluster
from api.utilities.geometry import parse_bbox
from localities.models import Country
from localities_osm.queries import all_locality


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

    def add_arguments(self, parser):
        parser.add_argument(
            '--country',
            dest='country',
            help='Country name',
        )

    def handle(self, *args, **options):
        country_name = options.get('country', None)

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

        osm_query = all_locality()
        for zoom in range(settings.CLUSTER_CACHE_MAX_ZOOM + 1):
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                '{}_{}_{}_localities.json'.format(zoom, *icon_size)
            )

            localities = osm_query.in_bbox(parse_bbox('-180,-90,180,90'))
            object_list = oms_view_cluster(localities, zoom, *icon_size)

            with open(filename, 'w') as f:
                json.dump(object_list, f)

            self.stdout.write('Generated cluster cache for zoom: %s' % zoom)

        countries = Country.objects.all()
        if country_name:
            countries = countries.filter(name__iexact=country_name)
        for country in countries:
            self.stdout.write('Generated cluster for %s' % country.name)
            localities = osm_query.in_administrative(country.get_codes)
            for zoom in range(settings.CLUSTER_CACHE_MAX_ZOOM + 1):
                filename = os.path.join(
                    settings.CLUSTER_CACHE_DIR,
                    '{}_{}_{}_localities_{}.json'.format(
                        zoom, icon_size[0], icon_size[1], country.name
                    )
                )

                object_list = oms_view_cluster(localities, zoom, *icon_size)

                with open(filename, 'w') as f:
                    json.dump(object_list, f)

                self.stdout.write('Generated cluster cache for zoom: %s' % zoom)
