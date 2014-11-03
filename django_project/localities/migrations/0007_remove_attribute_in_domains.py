# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0006_auto_20141103_0619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attribute',
            name='in_domains',
        ),
    ]
