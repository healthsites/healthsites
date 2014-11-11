# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0016_domainarchive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locality',
            name='created',
        ),
        migrations.RemoveField(
            model_name='locality',
            name='modified',
        ),
    ]
