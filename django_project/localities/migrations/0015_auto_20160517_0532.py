# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0014_auto_20160512_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataloader',
            name='data_loader_mode',
            field=models.IntegerField(help_text=b'The mode of the data loader.', verbose_name=b'Data Loader Mode', choices=[(1, b'Replace/Insert Data'), (2, b'Update Data')]),
        ),
    ]
