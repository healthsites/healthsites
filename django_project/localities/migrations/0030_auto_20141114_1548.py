# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0029_auto_20141114_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localityindex',
            name='locality',
            field=models.OneToOneField(to='localities.Locality'),
            preserve_default=True,
        ),
    ]
