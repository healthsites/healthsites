# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0005_auto_20160205_0738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='changeset',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='locality',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
