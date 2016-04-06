# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0007_auto_20160328_0843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataloader',
            name='organisation_name',
            field=models.CharField(help_text=b"Organiation's Name", max_length=100, verbose_name=b"Organisation's Name"),
        ),
    ]
