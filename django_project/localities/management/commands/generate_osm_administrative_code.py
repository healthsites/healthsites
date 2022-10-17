# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db.utils import ProgrammingError
from localities.models import Country
from localities_osm.models.locality import LocalityOSMNode, LocalityOSMWay


class Command(BaseCommand):
    help = 'Generate administrative code for osm'

    def add_arguments(self, parser):
        parser.add_argument(
            '--country',
            dest='country',
            help='Country name',
        )
        parser.add_argument(
            '--replace',
            dest='replace',
            help='Make everything to be reassigned',
        )

    def handle(self, *args, **options):
        country = options.get('country', None)
        replace = options.get('replace', False)
        replace = True if replace in ['True', 'true', 'y'] else replace

        countries = Country.objects.filter(parent__isnull=False)
        if country:
            countries = countries.filter(name__iexact=country)

        try:
            if replace:
                nodes = LocalityOSMNode.objects.all()
                ways = LocalityOSMWay.objects.all()
            else:
                nodes = LocalityOSMNode.objects.filter(administrative_code__isnull=True)
                ways = LocalityOSMWay.objects.filter(administrative_code__isnull=True)

            for country in countries:
                print(f'Reassign for country {country.code}')
                polygon = country.polygon_geometry
                nodes.in_polygon(polygon).update(administrative_code=country.code)
                ways.in_polygon(polygon).update(administrative_code=country.code)
        except ProgrammingError:
            pass
