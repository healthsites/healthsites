# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localities', '0018_auto_20141109_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='changeset',
            name='social_user',
            field=models.ForeignKey(default=-1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
