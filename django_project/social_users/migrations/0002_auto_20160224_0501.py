# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_picture', models.CharField(default=b'', max_length=150, blank=True)),
                ('screen_name', models.CharField(default=b'', max_length=50, blank=True)),
                ('user', models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserDetail',
        ),
    ]
