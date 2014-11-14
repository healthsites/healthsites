# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pg_fts.fields
from pg_fts.migrations import (
    CreateFTSIndexOperation,
    CreateFTSTriggerOperation
)


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0024_valuearchive'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocalityIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rankA', models.TextField(null=True)),
                ('rankB', models.TextField(null=True)),
                ('rankC', models.TextField(null=True)),
                ('rankD', models.TextField(null=True)),
                ('fts_index', pg_fts.fields.TSVectorField(dictionary='english', default='', fields=((b'rankA', b'A'), (b'rankB', b'B'), (b'rankC', b'C'), (b'rankD', b'D')), serialize=False, editable=False, null=True)),
                ('locality', models.ForeignKey(to='localities.Locality')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        CreateFTSIndexOperation(
            name='LocalityIndex',
            fts_vector='fts_index',
            index='gin'
        ),
        # create trigger to Article.fts_index
        CreateFTSTriggerOperation(
            name='LocalityIndex',
            fts_vector='fts_index'
        ),
    ]
