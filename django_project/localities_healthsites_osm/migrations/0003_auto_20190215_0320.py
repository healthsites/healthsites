# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_healthsites_osm', '0002_localityhealthsitesosm_certainty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localityhealthsitesosm',
            name='certainty',
        ),
        migrations.AddField(
            model_name='localityhealthsitesosm',
            name='osm_pk',
            field=models.BigIntegerField(null=True, blank=True),
        ),
    ]
