# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0008_auto_20160406_0603'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='completeness',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
