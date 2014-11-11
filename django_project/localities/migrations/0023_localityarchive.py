# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('localities', '0022_auto_20141111_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalityArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('domain_id', models.IntegerField()),
                ('uuid', models.TextField()),
                ('upstream_id', models.TextField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
