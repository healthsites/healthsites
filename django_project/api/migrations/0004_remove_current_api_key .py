# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def run(apps, schema_editor):
    UserApiKey = apps.get_model("api", "UserApiKey")
    UserApiKey.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0003_auto_20230406_0551')
    ]

    operations = [
        migrations.RunPython(run, migrations.RunPython.noop),
    ]
