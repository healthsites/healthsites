# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0026_specification_fts_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificationarchive',
            name='fts_rank',
            field=models.CharField(default='D', max_length=1),
            preserve_default=False,
        ),
    ]
