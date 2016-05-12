# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0012_auto_20160510_0406'),
    ]

    operations = [
        migrations.RenameField(
            model_name='synonymlocalities',
            old_name='locality_id',
            new_name='locality',
        ),
        migrations.RenameField(
            model_name='synonymlocalities',
            old_name='synonym_id',
            new_name='synonym',
        ),
        migrations.RenameField(
            model_name='unconfirmedsynonym',
            old_name='locality_id',
            new_name='locality',
        ),
        migrations.RenameField(
            model_name='unconfirmedsynonym',
            old_name='synonym_id',
            new_name='synonym',
        ),
        migrations.RemoveField(
            model_name='locality',
            name='synonyms',
        ),
        migrations.RemoveField(
            model_name='locality',
            name='unconfirmed_synonyms',
        ),
    ]
