# coding=utf-8
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/07/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.core.management.base import BaseCommand
import os
import shapefile
import zipfile
from django.conf import settings
from localities.models import Domain, Specification
from localities.utils import get_heathsites_master

directory = settings.CLUSTER_CACHE_DIR + "/facilities"


def zipdir(path, ziph):
    # ziph is zipfile handle
    abs_src = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            absname = os.path.abspath(os.path.join(root, file))
            arcname = absname[len(abs_src) + 1:]
            ziph.write(absname, arcname)


def insert_to_shapefile(healthsites):
    fields = [u'uuid', u'upstream', u'source', u'name', u'version', u'date_modified', u'completeness', u'source_url',
              u'raw-source']
    try:
        domain = Domain.objects.get(name="Health")
        specifications = Specification.objects.filter(domain=domain)

        for specification in specifications:
            fields.append(specification.attribute.key)

        # write world cache
        filename = os.path.join(directory, 'facilities')
        w = shapefile.Writer(shapefile.POINT)
        for field in fields:
            w.field(str(field), 'C', 100)

        # get from healthsites
        total = healthsites.count()
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
            print values
            w.point(dict['geom'][0], dict['geom'][1])
            w.record(*values)
            now += 1
        w.save(filename)
        # zip this output
        filename = os.path.join(settings.MEDIA_ROOT, "facilities_shapefile.zip")
        zipf = zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED)
        zipdir(directory, zipf)
        zipf.close()
    except Domain.DoesNotExist:
        pass


class Command(BaseCommand):
    help = 'generate shapefile for data in bulk'

    def handle(self, *args, **options):
        insert_to_shapefile(get_heathsites_master())
