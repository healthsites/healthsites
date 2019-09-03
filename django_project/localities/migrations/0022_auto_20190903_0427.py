# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0021_auto_20190719_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataloader',
            name='json_concept_mapping',
            field=models.FileField(help_text=b'JSON Concept Mapping File.', upload_to=b'json_mapping/%Y/%m/%d', null=True, verbose_name=b'JSON Concept Mapping', blank=True),
        ),
    ]
