# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0035_auto_20150907_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataloader',
            name='notes',
            field=models.TextField(default=b'', help_text=b'Notes', null=True, verbose_name=b'Notes', blank=True),
            preserve_default=True,
        ),
    ]
