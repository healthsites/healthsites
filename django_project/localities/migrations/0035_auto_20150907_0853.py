# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0034_auto_20150907_0849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataloader',
            name='date_time_applied',
            field=models.DateTimeField(help_text=b'When the data applied (loaded)', null=True, verbose_name=b'Applied (time)'),
            preserve_default=True,
        ),
    ]
