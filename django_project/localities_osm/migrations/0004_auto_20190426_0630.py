# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_osm', '0003_osm_facilities_view'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalityOSMExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('osm_id', models.BigIntegerField(db_index=True, null=True, blank=True)),
                ('osm_pk', models.BigIntegerField(null=True, blank=True)),
                ('osm_type', models.CharField(blank=True, max_length=30, null=True, choices=[(b'node', b'node'), (b'way', b'way'), (b'relation', b'relation')])),
            ],
            options={
                'ordering': ('osm_id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('value', models.CharField(max_length=512)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
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
        migrations.AddField(
            model_name='localityosmextension',
            name='custom_tag',
            field=models.ManyToManyField(to='localities_osm.Tag', blank=True),
        ),
    ]
