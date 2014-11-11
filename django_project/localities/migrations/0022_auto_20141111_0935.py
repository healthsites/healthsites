# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0021_specificationarchive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributearchive',
            name='object_id',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='domainarchive',
            name='object_id',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specificationarchive',
            name='object_id',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
