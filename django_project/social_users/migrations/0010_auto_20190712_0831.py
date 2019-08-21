# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('social_users', '0009_gatheruser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisationsupported',
            name='date_added',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
