# -*- coding: utf-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand

from localities.models import Country, Locality
import os
import json
from django.conf import settings
from localities.utils import get_statistic
from django.core.serializers.json import DjangoJSONEncoder
from localities.utils import get_heathsites_master


class Command(BaseCommand):
    """ Command for generate country cache.
    """
    help = 'Import Localities from CSV file'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            '--countries',
            dest='countries',
            help='Country name list with comma separator',
        )

    def handle(self, *args, **options):
        if options['countries']:
            countries = [countries_name for countries_name in options['countries'].split(',')]
            countries = Country.objects.filter(name__in=countries)
        else:
            countries = Country.objects.all()

        # check the folder
        if not os.path.exists(settings.CLUSTER_CACHE_DIR):
            os.makedirs(settings.CLUSTER_CACHE_DIR)

        try:
            # write world cache
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                'world_statistic')
            healthsites = get_heathsites_master().all()
            output = get_statistic(healthsites)
            result = json.dumps(output, cls=DjangoJSONEncoder)
            file = open(filename, 'w')
            file.write(result)  # python will convert \n to os.linesep
            file.close()  # you can omit in most cases as the destructor will call it
            print "world cache is finished"
        except Exception as ex:
            print "skip world"

        for country in countries:
            try:
                polygons = country.polygon_geometry

                # write country cache
                filename = os.path.join(
                    settings.CLUSTER_CACHE_DIR,
                    country.name + '_statistic'
                )
                healthsites = get_heathsites_master().in_polygon(
                    polygons)
                output = get_statistic(healthsites)
                result = json.dumps(output, cls=DjangoJSONEncoder)
                file = open(filename, 'w')
                file.write(result)  # python will convert \n to os.linesep
                file.close()  # you can omit in most cases as the destructor will call it
                print country.name + " cache is finished"
            except Exception as e:
                print e
                print "skip"
