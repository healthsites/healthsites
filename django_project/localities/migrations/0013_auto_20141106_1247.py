# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone

from django.db import models, migrations


def create_initial_changeset(apps, schema_editor):
    Changeset = apps.get_model('localities', 'Changeset')
    changeset = Changeset(pk=-1, created=timezone.now(), comment='migration')
    changeset.save()


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0012_changeset'),
    ]

    operations = [
        migrations.RunPython(create_initial_changeset),
    ]
