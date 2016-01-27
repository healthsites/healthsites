# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Christian Christelis <christian@kartoza.com>'
__project_name = 'watchkeeper'
__date__ = '8/05/15'
__copyright__ = 'kartoza.com'
__doc__ = ''


from django.db import models, migrations

from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import MultiPolygon, Polygon


def import_countries(apps, schema_editor):
    data_source = DataSource('localities/data/ne_10m_admin_0_countries.shp')
    Country = apps.get_model("localities", "Country")
    layer = data_source[0]
    for feature in layer:
        country_name = feature['NAME'].value
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
            country = Country(name=country_name, )
            country.polygon_geometry = geometry
        country.save()


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0002_country_province'),
    ]

    operations = [
        migrations.RunPython(import_countries),
    ]
