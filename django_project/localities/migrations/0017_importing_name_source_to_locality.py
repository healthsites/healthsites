# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from django.db import migrations


def localities_name_source_importer(apps, schema_editor):
    Locality = apps.get_model("localities", "Locality")
    Value = apps.get_model("localities", "Value")
    nonamed_localities = []
    for locality in Locality.objects.all():
        values = Value.objects.filter(locality=locality).filter(
            specification__attribute__key='name')
        if len(values) >= 1:
            locality.name = values[0].data
            if locality.name == "":
                nonamed_localities.append(locality.id)
        else:
            nonamed_localities.append(locality.id)

        values = Value.objects.filter(locality=locality).filter(
            specification__attribute__key='data_source')
        if len(values) >= 1:
            locality.source = values[0].data
        else:
            # exclusive for open street map
            if "openstreetmap" in locality.upstream_id:
                locality.source = "OpenStreetMap"
            else:
                locality.source = "healthsites.io"

        locality.save()
    Locality.objects.filter(id__in=nonamed_localities).delete()

    try:
        # delete name and data_source value
        Attribute = apps.get_model("localities", "Attribute")
        Attribute.objects.get(key='name').delete()
        Attribute.objects.get(key='data_source').delete()
    except:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('localities', '0016_auto_20160607_0611'),
    ]

    operations = [
        migrations.RunPython(localities_name_source_importer),
    ]
