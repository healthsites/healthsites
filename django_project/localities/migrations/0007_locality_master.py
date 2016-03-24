# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0006_auto_20160208_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='locality',
            name='master',
            field=models.ForeignKey(default=None, to='localities.Locality', null=True),
        ),
    ]
