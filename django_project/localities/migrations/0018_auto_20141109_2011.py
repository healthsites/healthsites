# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.contrib.auth import get_user_model


def create_bogus_user(apps, schema_editor):
    User = get_user_model()

    User.objects.create(username='__dummy__', id=-1)


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0017_auto_20141109_1850'),
    ]

    operations = [
        migrations.RunPython(create_bogus_user)
    ]
