# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0007_locality_master'),
    ]

    operations = [
        migrations.AddField(
            model_name='localityarchive',
            name='master',
            field=models.ForeignKey(default=None, to='localities.Locality', null=True),
        ),
    ]
