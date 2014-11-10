# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_specifications(apps, schema_editor):
    Domain = apps.get_model('localities', 'Domain')
    Specification = apps.get_model('localities', 'Specification')

    for dom in Domain.objects.all():
        for attr in dom.attribute_set.all():
            spec = Specification.objects.create(domain=dom, attribute=attr)
            spec.save()


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0005_auto_20141103_0618'),
    ]

    operations = [
        migrations.RunPython(migrate_specifications),
    ]
