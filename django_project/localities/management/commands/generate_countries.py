# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon
from localities.models import Country


class Command(BaseCommand):
    help = 'Import Localities from CSV file'
    non_countries = ["Scarborough Reef"]

    def handle(self, *args, **options):
        Country.objects.all().delete()
        data_source = DataSource('localities/data/ne_10m_admin_0_countries.shp')
        layer = data_source[0]
        for feature in layer:
            country_name = feature['NAME'].value
            country_name = country_name.encode('utf-8')

            # -------------------------------------------------
            # CORRECTING THE NAME
            # -------------------------------------------------
            country_name = country_name.replace(" (Petrel Is.)", "")
            country_name = country_name.replace("Barb.", "Barbuda")
            country_name = country_name.replace("Br.", "British")
            country_name = country_name.replace(
                "Central African Rep.", "Central African Republic"
            )
            country_name = country_name.replace("Curaçao", "Curacao")
            country_name = country_name.replace("Côte d'Ivoire", "Ivory Coast")
            country_name = country_name.replace(
                "Cyprus U.N. Buffer Zone", "United Nations Buffer Zone in Cyprus"
            )
            country_name = country_name.replace(
                "Dem. Rep. Congo", "Democratic Republic of the Congo"
            )
            country_name = country_name.replace("Dem. Rep. Korea", "North Korea")
            country_name = country_name.replace("Eq.", "Equatorial")
            country_name = country_name.replace(
                "Fr. S. Antarctic Lands", "French Southern and Antarctic Lands"
            )
            country_name = country_name.replace("Fr.", "French")
            country_name = country_name.replace("Geo.", "Georgia")
            country_name = country_name.replace("Gren.", "the Grenadines")
            country_name = country_name.replace("Herz.", "Herzegovina")
            country_name = country_name.replace("I.", "Islands")
            country_name = country_name.replace("Is.", "Islands")
            country_name = country_name.replace("N.", "Northern")
            country_name = country_name.replace("Rep.", "Republic")
            country_name = country_name.replace("U.S.", "United States")
            country_name = country_name.replace("S.", "South")
            country_name = country_name.replace("Sandw.", "Sandwich")
            country_name = country_name.replace("São Tomé and Principe", "Sao Tome and Principe")
            country_name = country_name.replace("St-Barthélemy", "Saint Barthelemy")
            country_name = country_name.replace("St.", "Saint")
            country_name = country_name.replace("St-", "Saint ")
            country_name = country_name.replace("Ter.", "Territory")
            country_name = country_name.replace("Vin.", "Vincent")
            country_name = country_name.replace("W.", "Western")

            country_name = country_name.strip()
            # -------------------------------------------------
            # FINISH
            # -------------------------------------------------

            geometry = feature.geom
            try:
                country = Country.objects.get(name=country_name)
                if 'MultiPolygon' not in geometry.geojson:
                    geometry = MultiPolygon(
                        [Polygon(coords) for coords in
                         country.geometry.coords[0]] +
                        [Polygon(geometry.coords[0])]).geojson
                else:
                    geometry = MultiPolygon(
                        [Polygon(coords) for coords in
                         country.geometry.coords[0]] +
                        [Polygon(coords) for coords in geometry.coords[0]]).geojson
                country.polygon_geometry = geometry
            except:
                if 'MultiPolygon' not in geometry.geojson:
                    geometry = MultiPolygon(Polygon(geometry.coords[0])).geojson
                else:
                    geometry = geometry.geojson
                country = Country(name=country_name)
                country.polygon_geometry = geometry
            if country_name not in self.non_countries:
                country.save()
