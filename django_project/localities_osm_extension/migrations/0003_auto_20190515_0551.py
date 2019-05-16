# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_osm_extension', '0002_auto_20190513_0550'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='localityosmextension',
            unique_together=set([('osm_id', 'osm_type')]),
        ),
    ]
