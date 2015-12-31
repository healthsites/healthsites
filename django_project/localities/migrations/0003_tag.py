# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0002_data_migration_20150521_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('tag', models.TextField()),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('locality', models.ForeignKey(to='localities.Locality')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
