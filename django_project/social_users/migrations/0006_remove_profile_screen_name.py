# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_users', '0005_auto_20160406_0603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='screen_name',
        ),
    ]
