# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('social_users', '0003_auto_20160330_0509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='website',
        ),
        migrations.AddField(
            model_name='organization',
            name='site',
            field=models.ForeignKey(default=None, to='sites.Site', null=True),
        ),
    ]
