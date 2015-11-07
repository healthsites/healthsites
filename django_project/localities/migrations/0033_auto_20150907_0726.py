# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0032_auto_20150806_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataloader',
            name='date_time_applied',
            field=models.DateTimeField(help_text=b'When the data applied (loaded)', null=True, verbose_name=b'Applied (time)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dataloader',
            name='date_time_uploaded',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 7, 7, 26, 22, 206, tzinfo=utc), help_text=b'When the data uploaded', verbose_name=b'Uploaded (time)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dataloader',
            name='separator',
            field=models.IntegerField(default=1, help_text=b'Separator character.', verbose_name=b'Separator Character', choices=[(1, b'Comma'), (2, b'Tab')]),
            preserve_default=True,
        ),
    ]
