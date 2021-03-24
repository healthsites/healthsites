# -*- coding: utf-8 -*-
import os
import shutil
import zipfile

import shapefile

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Polygon
from django.forms.models import fields_for_model

from localities.models import Country
from localities_osm.models.locality import LocalityOSM, LocalityOSMView  # noqa
from localities_osm.queries import filter_locality

directory_cache = settings.CACHE_DIR
directory_media = settings.SHAPEFILE_DIR


def zipdir(path, ziph):
    # ziph is zipfile handle
    abs_src = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            absname = os.path.abspath(os.path.join(root, file))
            arcname = absname[len(abs_src) + 1:]
            ziph.write(absname, arcname)


# funtion to generate a .prj file
def getWKT_PRJ(epsg_code):
    import urllib
    wkt = \
        urllib.urlopen(
            'http://spatialreference.org/ref/epsg/{0}/prettywkt/'.format(
                epsg_code))
    remove_spaces = wkt.read().replace(' ', '')
    output = remove_spaces.replace('\n', '')
    return output


def get_shapefile_folder(counter_name):
    """ Return shapefile folder for a country"""
    shp_filename = counter_name.replace('.', '')
    return os.path.join(directory_cache, 'shapefiles', shp_filename)


def country_data_into_shapefile(country=None):
    """ Convert country osm data into shapefile

    :param country: Country name
    :type: str
    """
    if country == 'World' or country == 'world':
        country = None
    queryset = filter_locality(
        extent=None,
        country=country).order_by('row')
    country_name = 'World'
    if country:
        country_name = country

    # get field that needs to be saved
    fields = fields_for_model(LocalityOSM).keys()

    # get the folders
    shp_filename = country_name.replace('.', '')
    dir_cache = get_shapefile_folder(country_name)
    dir_shapefile = os.path.join(dir_cache, 'output')

    # delete the cache
    try:
        shutil.rmtree(dir_shapefile)
    except OSError:
        pass

    # generate the node shapefile
    insert_to_shapefile(
        query=queryset.filter(osm_type=LocalityOSMView.NODE),
        fields=fields,
        dir_shapefile=dir_shapefile,
        shp_filename=u'{}-node'.format(shp_filename),
        TYPE=shapefile.POINT)

    # generate the way shapefile
    insert_to_shapefile(
        query=queryset.filter(osm_type=LocalityOSMView.WAY),
        fields=fields,
        dir_shapefile=dir_shapefile,
        shp_filename=u'{}-way'.format(shp_filename),
        TYPE=shapefile.POLYGON)

    # zip this output
    print 'rezipping the files'
    if not os.path.exists(directory_media):
        os.makedirs(directory_media)
    filename = os.path.join(directory_media, '%s.zip' % country_name)
    try:
        os.remove(filename)
    except OSError:
        pass

    zipf = zipfile.ZipFile(filename, 'w', allowZip64=True)
    zipdir(dir_shapefile, zipf)
    zipf.close()

    try:
        shutil.rmtree(dir_cache)
    except OSError:
        pass


def insert_to_shapefile(query, fields, dir_shapefile, shp_filename, TYPE):
    """ Convert and insert data into shapefile
    """
    from localities_osm.serializer.locality_osm import (
        LocalityOSMGeoSerializer
    )

    # Insert data into shapefile
    print 'generating shape object for ' + shp_filename

    shapefile_output = os.path.join(dir_shapefile, shp_filename)
    shp = shapefile.Writer(shapefile_output, TYPE)
    for field in fields:
        shp.field(str(field), 'C', 100)

    # insert data
    for healthsite_obj in query:
        values = []
        healthsite = LocalityOSMGeoSerializer(healthsite_obj).data
        properties = healthsite['properties']
        if not properties['centroid'] or not properties['centroid']['coordinates']:
            continue
        for field in fields:
            value = ''
            if field in properties['attributes']:
                value = properties['attributes'][field]
            elif field in properties:
                value = properties[field]

            try:
                value = str(value.encode('utf8'))
            except AttributeError:
                pass
            values.append(value)

        if not values:
            continue

        if TYPE == shapefile.POINT:
            shp.point(
                properties['centroid']['coordinates'][0],
                properties['centroid']['coordinates'][1])
        elif TYPE == shapefile.POLYGON:
            coordinates = healthsite['geometry']['coordinates']
            if isinstance(healthsite_obj.geometry, Polygon):
                shp.poly(coordinates)
            else:
                shp.poly(coordinates[0])
        shp.record(*values)

    shp.close()

    # create .cpg
    cpg_file = os.path.join(dir_shapefile, shp_filename + '.cpg')
    file = open(cpg_file, 'w+')
    file.write('UTF-8')
    file.close()

    # create .prj
    prj_file = os.path.join(dir_shapefile, shp_filename + '.prj')
    prj = open(prj_file, 'w+')
    epsg = getWKT_PRJ('4326')
    prj.write(epsg)
    prj.close()


class Command(BaseCommand):
    help = 'generate shapefile for data in bulk'

    def add_arguments(self, parser):
        parser.add_argument(
            '--country',
            help='country name',
        )

    def handle(self, *args, **options):
        country = options.get('country', None)

        # generate shapefiles for world
        if not country or country.lower() == 'world':
            try:
                country_data_into_shapefile('')
            except Exception as e:
                print '{}'.format(e)

        # generate shapefiles for countries
        countries = Country.objects.all()
        if country:
            countries = countries.filter(name__iexact=country)

        countries = countries.order_by('name')
        for country in countries:
            # generate shapefiles for country
            try:
                country_data_into_shapefile(country.name)
            except Exception as e:
                print '{}'.format(e)
