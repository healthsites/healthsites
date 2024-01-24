# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_users', '0008_organisation_organizer'),
    ]

    operations = [
        migrations.CreateModel(
            name='GatherUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gather_id', models.IntegerField()),
                ('gather_password', models.CharField(max_length=512)),
                ('user', models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL, on_delete=django.db.models.deletion.CASCADE)),
            ],
        ),
    ]
