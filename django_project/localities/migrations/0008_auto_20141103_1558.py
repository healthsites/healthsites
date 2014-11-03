# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0007_remove_attribute_in_domains'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='specifications',
            field=models.ManyToManyField(to='localities.Specification', through='localities.Value'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='value',
            name='specification',
            field=models.ForeignKey(default=1, to='localities.Specification'),
            preserve_default=False,
        ),
    ]
