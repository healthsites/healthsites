# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userapikey',
            name='allow_write',
            field=models.BooleanField(default=False, help_text=b'allow this api key to write data'),
        ),
    ]
