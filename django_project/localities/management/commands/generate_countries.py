# -*- coding: utf-8 -*-

import json
from django.contrib.gis.db.models import Union
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.core.management.base import BaseCommand

from localities.models import Country


class Command(BaseCommand):
    help = 'Generate country boundaries from SHP file'
    non_countries = ['Scarborough Reef']

    def handle(self, *args, **options):
        country_by_code = {}
        with open('localities/data/osm_boundaries/country_data.json') as file:
            data = json.load(file)
            for country in data:
                if country['Three_Letter_Country_Code']:
                    country_by_code[country['Three_Letter_Country_Code']] = country

        Country.objects.all().delete()
        data_source = DataSource(
            'localities/data/osm_boundaries/country_boundaries.shp')
        layer = data_source[0]
        for feature in layer:
            country_name = feature['name'].value
            country_code = feature['country'].value

            print u'processing {} ({})'.format(country_name, country_code)
            try:
                country_data = country_by_code[country_code]
            except KeyError:
                print u'{} ({}) is not found'.format(country_name, country_code)
                continue
            # print country_data
            country_name = country_name.encode('utf-8')

            # -------------------------------------------------
            # CORRECTING THE NAME
            # -------------------------------------------------
            country_name = country_name.replace(' (Petrel Is.)', '')
            country_name = country_name.replace('Barb.', 'Barbuda')
            country_name = country_name.replace('Br.', 'British')
            country_name = country_name.replace(
                'Central African Rep.', 'Central African Republic'
            )
            country_name = country_name.replace('Curaçao', 'Curacao')
            country_name = country_name.replace('Côte d\'Ivoire', 'Ivory Coast')  # noqa
            country_name = country_name.replace(
                'Cyprus U.N. Buffer Zone',
                'United Nations Buffer Zone in Cyprus'
            )
            country_name = country_name.replace(
                'Dem. Rep. Congo', 'Democratic Republic of the Congo'
            )
            country_name = country_name.replace(
                'Dem. Rep. Korea', 'North Korea')
            country_name = country_name.replace('Eq.', 'Equatorial')
            country_name = country_name.replace(
                'Fr. S. Antarctic Lands', 'French Southern and Antarctic Lands'
            )
            country_name = country_name.replace('Fr.', 'French')
            country_name = country_name.replace('Geo.', 'Georgia')
            country_name = country_name.replace('Gren.', 'the Grenadines')
            country_name = country_name.replace('Herz.', 'Herzegovina')
            country_name = country_name.replace('I.', 'Islands')
            country_name = country_name.replace('Is.', 'Islands')
            country_name = country_name.replace('N.', 'Northern')
            country_name = country_name.replace('Rep.', 'Republic')
            country_name = country_name.replace('U.S.', 'United States')
            country_name = country_name.replace('S.', 'South')
            country_name = country_name.replace('Sandw.', 'Sandwich')
            country_name = country_name.replace(
                'São Tomé and Principe', 'Sao Tome and Principe')
            country_name = country_name.replace(
                'St-Barthélemy', 'Saint Barthelemy')
            country_name = country_name.replace('St.', 'Saint')
            country_name = country_name.replace('St-', 'Saint ')
            country_name = country_name.replace('Ter.', 'Territory')
            country_name = country_name.replace('Vin.', 'Vincent')
            country_name = country_name.replace('W.', 'Western')
            country_name = country_name.strip()

            print 'generate {}'.format(country_name)

            geometry = feature.geom
            try:
                country = Country.objects.get(name=country_name)
                if 'MultiPolygon' not in geometry.geojson:
                    polygons = \
                        [Polygon(coords)
                         for coords in country.geometry.coords[0]]
                    polygons += [Polygon(geometry.coords[0])]
                    geometry = MultiPolygon(polygons).geojson
                else:
                    polygons = \
                        [Polygon(coords)
                         for coords in country.geometry.coords[0]]
                    polygons += \
                        [Polygon(coords) for coords in geometry.coords[0]]
                    geometry = MultiPolygon(polygons).geojson
                geometry = geometry
            except Exception:
                if 'MultiPolygon' not in geometry.geojson:
                    geometry = \
                        MultiPolygon(Polygon(geometry.coords[0])).geojson
                else:
                    geometry = geometry.geojson
                geometry = geometry

            # create the continent
            continent, created = Country.objects.get_or_create(
                name=country_data['Continent_Name'],
                defaults={
                    'code': country_data['Continent_Code']
                }

            )
            # create country
            Country.objects.get_or_create(
                name=country_name,
                defaults={
                    'polygon_geometry': geometry,
                    'code': country_data['Three_Letter_Country_Code'],
                    'parent': continent
                }
            )

        # create geometry for continent
        for country in Country.objects.filter(polygon_geometry__isnull=True):
            print u'processing {}'.format(country.name)
            country.polygon_geometry = Country.objects.filter(parent=country).aggregate(
                geometry=Union('polygon_geometry'))['geometry'].buffer(0.0000001)
            country.save()
