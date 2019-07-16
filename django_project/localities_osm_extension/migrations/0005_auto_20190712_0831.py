# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localities_osm_extension', '0004_pendingstate'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('reason', models.TextField(default=b'', null=True, blank=True)),
                ('payload', models.TextField(default=b'', null=True, blank=True)),
                ('time_uploaded', models.DateTimeField(auto_now_add=True)),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PendingUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_uploaded', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=512)),
                ('version', models.IntegerField()),
                ('extension', models.OneToOneField(to='localities_osm_extension.LocalityOSMExtension')),
                ('uploader', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='pendingstate',
            name='extension',
        ),
        migrations.RemoveField(
            model_name='pendingstate',
            name='uploader',
        ),
        migrations.DeleteModel(
            name='PendingState',
        ),
    ]
