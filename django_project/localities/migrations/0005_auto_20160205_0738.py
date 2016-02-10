# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0004_datahistory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datahistory',
            name='author',
        ),
        migrations.RemoveField(
            model_name='datahistory',
            name='locality',
        ),
        migrations.DeleteModel(
            name='DataHistory',
        ),
    ]
