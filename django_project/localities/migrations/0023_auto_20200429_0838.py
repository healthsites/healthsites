# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0022_auto_20190903_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='code',
            field=models.CharField(help_text=b'administrative code', max_length=32, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='country',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='localities.Country', help_text=b'is the administrative under other administrative (parent)', null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='polygon_geometry',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True, blank=True),
        ),
    ]
