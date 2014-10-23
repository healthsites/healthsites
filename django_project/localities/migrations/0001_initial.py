# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.TextField(unique=True)),
                ('upstream_id', models.TextField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField(blank=True)),
                ('attribute', models.ForeignKey(to='localities.Attribute')),
                ('locality', models.ForeignKey(to='localities.Locality')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='locality',
            name='attributes',
            field=models.ManyToManyField(to='localities.Attribute', through='localities.Value'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='locality',
            name='group',
            field=models.ForeignKey(to='localities.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attribute',
            name='in_group',
            field=models.ManyToManyField(to='localities.Group'),
            preserve_default=True,
        ),
    ]
