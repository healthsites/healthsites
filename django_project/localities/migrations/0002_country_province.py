# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name', models.CharField(help_text=b'The name of the country.', max_length=50, verbose_name=b'')),
                ('polygon_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('name', models.CharField(help_text=b'The name of the province or state.', max_length=50, verbose_name=b'')),
                ('polygon_geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('country', models.ForeignKey(to='localities.Country')),
            ],
            options={
                'verbose_name_plural': 'Provinces',
            },
        ),
    ]
