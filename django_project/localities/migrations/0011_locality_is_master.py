# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0010_auto_20160510_0249'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='is_master',
            field=models.BooleanField(default=True),
        ),
    ]
