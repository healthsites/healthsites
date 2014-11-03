# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0010_auto_20141103_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='value',
            name='attribute',
        ),
    ]
