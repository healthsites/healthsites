# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0017_importing_name_source_to_locality'),
    ]

    operations = [
        migrations.AddField(
            model_name='localityarchive',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='localityarchive',
            name='source',
            field=models.TextField(default=b'healthsites.io'),
        ),
        migrations.AlterField(
            model_name='locality',
            name='source',
            field=models.TextField(default=b'healthsites.io'),
        ),
    ]
