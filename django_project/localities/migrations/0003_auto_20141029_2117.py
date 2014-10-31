# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0002_group_template_fragment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='Domain',
        ),
        migrations.RenameField(
            model_name='attribute',
            old_name='in_groups',
            new_name='in_domains',
        ),
        migrations.RenameField(
            model_name='locality',
            old_name='group',
            new_name='domain',
        ),
    ]
