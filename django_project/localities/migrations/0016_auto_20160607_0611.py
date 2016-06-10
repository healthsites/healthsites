# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0015_auto_20160517_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locality',
            name='source',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
