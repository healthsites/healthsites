# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_users', '0007_auto_20190521_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='organizer',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.CASCADE),
        ),
    ]
