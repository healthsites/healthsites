# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_healthsites_osm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='localityhealthsitesosm',
            name='certainty',
            field=models.BooleanField(default=False),
        ),
    ]
