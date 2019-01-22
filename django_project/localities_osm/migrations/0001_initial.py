# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LocalityOSMNode',
            fields=[
                ('osm_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=512, null=True, blank=True)),
                ('name', models.CharField(max_length=512, null=True, blank=True)),
                ('emergency', models.CharField(max_length=512, null=True, blank=True)),
                ('operator', models.CharField(max_length=512, null=True, blank=True)),
                ('opening_hours', models.CharField(max_length=512, null=True, blank=True)),
                ('contact_website', models.CharField(max_length=512, null=True, blank=True)),
                ('contact_phone', models.CharField(max_length=512, null=True, blank=True)),
                ('phone', models.CharField(max_length=512, null=True, blank=True)),
                ('website', models.CharField(max_length=512, null=True, blank=True)),
                ('speciality', models.CharField(max_length=512, null=True, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'osm_healthcare_facilities_node',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LocalityOSMView',
            fields=[
                ('osm_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=512, null=True, blank=True)),
                ('name', models.CharField(max_length=512, null=True, blank=True)),
                ('emergency', models.CharField(max_length=512, null=True, blank=True)),
                ('operator', models.CharField(max_length=512, null=True, blank=True)),
                ('opening_hours', models.CharField(max_length=512, null=True, blank=True)),
                ('contact_website', models.CharField(max_length=512, null=True, blank=True)),
                ('contact_phone', models.CharField(max_length=512, null=True, blank=True)),
                ('phone', models.CharField(max_length=512, null=True, blank=True)),
                ('website', models.CharField(max_length=512, null=True, blank=True)),
                ('speciality', models.CharField(max_length=512, null=True, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'osm_healthcare_facilities',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LocalityOSMWay',
            fields=[
                ('osm_id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=512, null=True, blank=True)),
                ('name', models.CharField(max_length=512, null=True, blank=True)),
                ('emergency', models.CharField(max_length=512, null=True, blank=True)),
                ('operator', models.CharField(max_length=512, null=True, blank=True)),
                ('opening_hours', models.CharField(max_length=512, null=True, blank=True)),
                ('contact_website', models.CharField(max_length=512, null=True, blank=True)),
                ('contact_phone', models.CharField(max_length=512, null=True, blank=True)),
                ('phone', models.CharField(max_length=512, null=True, blank=True)),
                ('website', models.CharField(max_length=512, null=True, blank=True)),
                ('speciality', models.CharField(max_length=512, null=True, blank=True)),
                ('geometry', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, blank=True)),
            ],
            options={
                'db_table': 'osm_healthcare_facilities_way',
                'managed': False,
            },
        ),
    ]
