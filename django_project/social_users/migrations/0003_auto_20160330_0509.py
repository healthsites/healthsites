# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social_users', '0002_auto_20160224_0501'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_added', models.DateField()),
                ('invite_reason', models.CharField(max_length=64, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('website', models.CharField(default=b'', max_length=64, blank=True)),
                ('contact', models.CharField(default=b'', max_length=64, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrustedUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organizations', models.ManyToManyField(to='social_users.Organization', through='social_users.Membership', blank=True)),
                ('user', models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='trusted_users',
            field=models.ManyToManyField(to='social_users.TrustedUser', through='social_users.Membership', blank=True),
        ),
        migrations.AddField(
            model_name='membership',
            name='organisation',
            field=models.ForeignKey(to='social_users.Organization'),
        ),
        migrations.AddField(
            model_name='membership',
            name='user',
            field=models.ForeignKey(to='social_users.TrustedUser'),
        ),
    ]
