# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('localities_osm', '0005_auto_20211227_0418'),
    ]

    operations = [
        migrations.AddField(
            model_name='localityosmnode',
            name='administrative_code',
            field=models.CharField(blank=True, null=True, max_length=32, help_text='Administrative code'),
        ),
        migrations.AddField(
            model_name='localityosmway',
            name='administrative_code',
            field=models.CharField(blank=True, null=True, max_length=32, help_text='Administrative code'),
        ),
    ]
