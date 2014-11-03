# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_specifications(apps, schema_editor):
    Value = apps.get_model('localities', 'Value')
    Specification = apps.get_model('localities', 'Specification')

    for val in Value.objects.all():
        spec = Specification.objects.get(
            attribute=val.attribute, domain=val.locality.domain
        )
        val.specification = spec
        val.save()


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0008_auto_20141103_1558'),
    ]

    operations = [
        migrations.RunPython(migrate_specifications),
    ]
