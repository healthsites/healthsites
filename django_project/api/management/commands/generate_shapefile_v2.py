# -*- coding: utf-8 -*-
import os
import shutil
import zipfile

import shapefile
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.forms.models import fields_for_model

from localities.models import Country
from localities_osm.models.locality import LocalityOSM, LocalityOSMView
from localities_osm.serializer.locality_osm import (
    LocalityOSMSerializer
)

directory_cache = settings.CACHE_DIR
directory_media = settings.MEDIA_ROOT + '/shapefiles'


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
    wkt = urllib.urlopen('http://spatialreference.org/ref/epsg/{0}/prettywkt/'.format(epsg_code))
    remove_spaces = wkt.read().replace(' ', '')
    output = remove_spaces.replace('\n', '')
    return output


def country_data_into_shapefile(country):
    """ Convert country osm data into shapefile

    :param country_name: Country name
    :type: str
    """
    country_name = 'World'
    if country == 'World':
        queryset = LocalityOSMView.objects.all().order_by('row')
    else:
        country = Country.objects.get(
            name__iexact=country)
        country_name = country.name
        polygons = country.polygon_geometry
        queryset = LocalityOSMView.objects.in_polygon(polygons).order_by('row')

    # get field that needs to be saved
    fields = fields_for_model(LocalityOSM).keys()
    insert_to_shapefile(
        LocalityOSMSerializer(queryset, many=True).data, fields, country_name)


def insert_to_shapefile(data, fields, shp_filename):
    """ Convert and insert data into shapefile
    :param data: data that will be inserted
    :param shp_filename: shapefile name
    """
    dir_cache = os.path.join(directory_cache, shp_filename)
    dir_shapefile = os.path.join(dir_cache, 'output')
    metadata_file = os.path.join(dir_cache, 'metadata')

    try:
        shutil.rmtree(dir_cache)
    except OSError:
        pass

    # this indicated that other generation process is run
    os.makedirs(dir_shapefile)

    # Insert data into shapefile
    print 'generating shape object for ' + shp_filename

    shapefile_output = os.path.join(dir_shapefile, shp_filename)
    shp = shapefile.Writer(shapefile_output, shapefile.POINT)
    for field in fields:
        shp.field(str(field), 'C', 100)

    total = len(data)
    for index, healthsite in enumerate(data):
        values = []
        # if centroid is None
        if not healthsite['centroid']:
            total -= 1
            continue

        for field in fields:
            value = ''
            if field in healthsite['attributes']:
                value = healthsite['attributes'][field]
            elif field in healthsite:
                value = healthsite[field]

            try:
                value = str(value.encode('utf8'))
            except AttributeError:
                pass
            values.append(value)
        shp.point(
            healthsite['centroid']['coordinates'][0],
            healthsite['centroid']['coordinates'][1])
        shp.record(*values)

        # save the process
        try:
            file = open(metadata_file, 'w+')
            file.write(json.dumps({
                'index': index + 1,
                'total': total,
                'last': healthsite['osm_id']
            }))
            file.close()
        except Exception as e:
            pass
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

    # zip this output
    print 'rezipping the files'
    if not os.path.exists(directory_media):
        os.makedirs(directory_media)
    filename = os.path.join(directory_media, '%s.zip' % shp_filename)
    try:
        os.remove(filename)
    except OSError:
        pass

    zipf = zipfile.ZipFile(filename, 'w', allowZip64=True)
    zipdir(dir_shapefile, zipf)
    zipf.close()


class Command(BaseCommand):
    help = 'generate shapefile for data in bulk'

    def handle(self, *args, **options):
        countries = Country.objects.all().order_by('name')
        for country in countries:
            # generate shapefiles for country
            country_data_into_shapefile(country.name)

        # generate shapefiles for all country
        country_data_into_shapefile('World')
