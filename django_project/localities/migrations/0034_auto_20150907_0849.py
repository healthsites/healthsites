# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0033_auto_20150907_0726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataloader',
            name='date_time_uploaded',
            field=models.DateTimeField(help_text=b'Timestamp (UTC) when the data uploaded', verbose_name=b'Uploaded (time)'),
            preserve_default=True,
        ),
    ]
