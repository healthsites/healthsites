# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0014_auto_20141106_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='version',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain',
            name='version',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locality',
            name='version',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specification',
            name='version',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='value',
            name='version',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
