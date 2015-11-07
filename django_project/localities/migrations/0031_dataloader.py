# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localities', '0030_auto_20141114_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataLoader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ("Organization's Name", models.CharField(help_text=b"Organization's Name", max_length=100)),
                ('JSON Concept Mapping', models.FileField(help_text=b'JSON Concept Mapping File.', upload_to=b'json_mapping/%Y/%m/%d')),
                ('CSV Data', models.FileField(help_text=b'CSV data that contains the data.', upload_to=b'csv_data/%Y/%m/%d')),
                ('data_loader_mode', models.IntegerField(help_text=b'The mode of the data loader.', verbose_name=b'Data Loader Mode', choices=[(1, b'Replace Data'), (2, b'Update Data')])),
                ('applied', models.BooleanField(default=False, help_text=b'Whether the data update has been applied or not.', verbose_name=b'Applied')),
                ('author', models.ForeignKey(verbose_name=b'Author', to=settings.AUTH_USER_MODEL, help_text=b'The user who propose the data loader.')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
