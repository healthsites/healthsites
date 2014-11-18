# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0025_localityindex'),
    ]

    operations = [
        migrations.AddField(
            model_name='specification',
            name='fts_rank',
            field=models.CharField(default=b'D', max_length=1, choices=[(b'A', b'Rank A'), (b'B', b'Rank B'), (b'C', b'Rank C'), (b'D', b'Rank D')]),
            preserve_default=True,
        ),
    ]
