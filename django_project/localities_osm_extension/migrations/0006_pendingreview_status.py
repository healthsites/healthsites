# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_osm_extension', '0005_auto_20190712_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='pendingreview',
            name='status',
            field=models.CharField(default=b'ERROR', max_length=30, choices=[(b'ERROR', b'ERROR'), (b'DRAFT', b'DRAFT')]),
        ),
    ]
