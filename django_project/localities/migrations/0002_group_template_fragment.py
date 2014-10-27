# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='template_fragment',
            field=models.TextField(default=b'', null=True, blank=True),
            preserve_default=True,
        ),
    ]
