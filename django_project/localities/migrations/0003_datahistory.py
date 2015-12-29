# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0002_data_migration_20150521_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_loader', models.ForeignKey(to='localities.DataLoader')),
                ('locality', models.ForeignKey(to='localities.Locality')),
            ],
        ),
    ]
