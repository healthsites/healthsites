# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0018_auto_20160609_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='migrated',
            field=models.BooleanField(default=False),
        ),
    ]
