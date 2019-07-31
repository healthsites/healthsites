# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0020_auto_20190712_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataloader',
            name='data_loader_mode',
            field=models.IntegerField(default=1, help_text=b'The mode of the data loader.', verbose_name=b'Data Loader Mode', choices=[(1, b'Replace/Insert Data'), (2, b'Update Data')]),
        ),
        migrations.AlterField(
            model_name='dataloader',
            name='organisation_name',
            field=models.CharField(default=b'', max_length=100, blank=True, help_text=b"Organisation's Name", null=True, verbose_name=b"Organisation's Name"),
        ),
    ]
