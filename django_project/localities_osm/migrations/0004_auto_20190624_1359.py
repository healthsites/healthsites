# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_osm', '0003_osm_facilities_view'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='localityosmnode',
            options={'managed': False, 'verbose_name': 'OSM Node', 'verbose_name_plural': 'OSM Node'},
        ),
        migrations.AlterModelOptions(
            name='localityosmview',
            options={'managed': False, 'verbose_name': 'OSM Node and Way', 'verbose_name_plural': 'OSM Node and Way'},
        ),
        migrations.AlterModelOptions(
            name='localityosmway',
            options={'managed': False, 'verbose_name': 'OSM Way', 'verbose_name_plural': 'OSM Way'},
        ),
    ]
