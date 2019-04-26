# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
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
        migrations.AddField(
            model_name='localityosmextension',
            name='custom_tag',
            field=models.ManyToManyField(to='locality_osm_extension.Tag', blank=True),
        ),
    ]
