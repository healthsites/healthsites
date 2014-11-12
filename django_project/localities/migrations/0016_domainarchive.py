# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('localities', '0015_auto_20141106_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
                ('template_fragment', models.TextField(null=True, blank=True)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
