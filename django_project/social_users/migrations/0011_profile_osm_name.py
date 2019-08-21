# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_users', '0010_auto_20190712_0831'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='osm_name',
            field=models.CharField(default=b'', max_length=512, blank=True),
        ),
    ]
