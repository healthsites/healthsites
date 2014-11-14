# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pg_fts.fields


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0027_specificationarchive_fts_rank'),
    ]

    operations = [
        migrations.RenameField(
            model_name='localityindex',
            old_name='rankA',
            new_name='ranka',
        ),
        migrations.RenameField(
            model_name='localityindex',
            old_name='rankB',
            new_name='rankb',
        ),
        migrations.RenameField(
            model_name='localityindex',
            old_name='rankC',
            new_name='rankc',
        ),
        migrations.RenameField(
            model_name='localityindex',
            old_name='rankD',
            new_name='rankd',
        ),
        migrations.AlterField(
            model_name='localityindex',
            name='fts_index',
            field=pg_fts.fields.TSVectorField(dictionary='english', default='', fields=((b'ranka', b'A'), (b'rankb', b'B'), (b'rankc', b'C'), (b'rankd', b'D')), serialize=False, editable=False, null=True),
            preserve_default=True,
        ),
    ]
