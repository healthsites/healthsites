# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0009_locality_completeness'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locality',
            name='master',
        ),
        migrations.RemoveField(
            model_name='localityarchive',
            name='master',
        ),
    ]
