# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0009_auto_20141103_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locality',
            name='attributes',
        ),
        migrations.AlterUniqueTogether(
            name='value',
            unique_together=set([('locality', 'specification')]),
        ),
    ]
