# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0031_dataloader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataloader',
            name='CSV Data',
        ),
        migrations.RemoveField(
            model_name='dataloader',
            name='JSON Concept Mapping',
        ),
        migrations.RemoveField(
            model_name='dataloader',
            name="Organization's Name",
        ),
        migrations.AddField(
            model_name='dataloader',
            name='csv_data',
            field=models.FileField(default='', help_text=b'CSV data that contains the data.', verbose_name=b'CSV Data', upload_to=b'csv_data/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataloader',
            name='json_concept_mapping',
            field=models.FileField(default='', help_text=b'JSON Concept Mapping File.', verbose_name=b'JSON Concept Mapping', upload_to=b'json_mapping/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataloader',
            name='organisation_name',
            field=models.CharField(default='', help_text=b"Organization's Name", max_length=100, verbose_name=b"Organization's Name"),
            preserve_default=False,
        ),
    ]
