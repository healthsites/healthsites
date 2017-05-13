# -*- coding: utf-8 -*-
import os
import shutil
import zipfile

import shapefile

from django.conf import settings
from django.core.management.base import BaseCommand

from localities.models import Country, Domain, Specification
from localities.utils import get_heathsites_master

directory_cache = settings.CLUSTER_CACHE_DIR + "/shapefiles"
directory_media = settings.MEDIA_ROOT + "/shapefiles"


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
    wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    remove_spaces = wkt.read().replace(" ", "")
    output = remove_spaces.replace("\n", "")
    return output


def insert_to_shapefile(healthsites, fields, shp_filename):
    try:
        dir_cache = os.path.join(directory_cache, shp_filename)

        # this indicated that other generation process is run
        if not os.path.exists(dir_cache):
            # create directory
            os.makedirs(dir_cache)

            # get healthsites data
            total = healthsites.count()
            if total > 0:
                # just for healthsite that total more than 0
                print "generating shape object for " + shp_filename

                shp = None
                shp = shapefile.Writer(shapefile.POINT)
                for field in fields:
                    shp.field(str(field), 'C', 100)

                now = 1
                for healthsite in healthsites:
                    values = []
                    dict = healthsite.repr_dict(clean=True)
                    for field in fields:
                        value = ""
                        if field in dict:
                            value = dict[field]
                        elif field in dict['values']:
                            value = dict['values'][field]
                        try:
                            value = str(value.encode('utf8'))
                        except AttributeError:
                            pass
                        values.append(value)
                    print "converted %d / %d" % (now, total)
                    shp.point(dict['geom'][0], dict['geom'][1])
                    shp.record(*values)
                    now += 1

                shapefile_output = os.path.join(dir_cache, shp_filename)
                shp.save(shapefile_output)

                # create .cpg
                cpg_file = os.path.join(dir_cache, shp_filename + ".cpg")
                file = open(cpg_file, 'w+')
                file.write("UTF-8")
                file.close()

                # create .prj
                prj_file = os.path.join(dir_cache, shp_filename + ".prj")
                prj = open(prj_file, "w+")
                epsg = getWKT_PRJ("4326")
                prj.write(epsg)
                prj.close()

                # zip this output
                print "rezipping the files"
                if not os.path.exists(directory_media):
                    os.makedirs(directory_media)

                filename = os.path.join(directory_media, shp_filename + "_shapefile.zip")
                os.remove(filename)

                zipf = zipfile.ZipFile(filename, 'w', allowZip64=True)
                zipdir(dir_cache, zipf)
                zipf.close()
                print "done"
            shutil.rmtree(dir_cache)
    except Domain.DoesNotExist:
        pass


class Command(BaseCommand):
    help = 'generate shapefile for data in bulk'

    def handle(self, *args, **options):
        domain = Domain.objects.get(name="Health")
        specifications = Specification.objects.filter(domain=domain)

        fields = [
            u'uuid', u'upstream',
            u'source', u'name', u'version',
            u'date_modified', u'completeness',
            u'source_url', u'raw-source']

        for specification in specifications:
            fields.append(specification.attribute.key)

        countries = Country.objects.all().order_by('name')
        for country in countries:
            polygons = country.polygon_geometry
            # query for each of ATTRIBUTE
            healthsites = get_heathsites_master().in_polygon(
                polygons)
            # generate shapefiles for country
            insert_to_shapefile(healthsites, fields, country.name)

        # generate shapefiles for all country
        insert_to_shapefile(get_heathsites_master(), fields, 'facilities')
