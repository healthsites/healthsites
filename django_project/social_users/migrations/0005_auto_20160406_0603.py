# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        ('social_users', '0004_auto_20160331_1008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('contact', models.CharField(default=b'', max_length=64, blank=True)),
                ('site', models.ForeignKey(default=None, to='sites.Site', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrganisationSupported',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name=b'Is Staff')),
                ('date_added', models.DateField()),
                ('organisation', models.ForeignKey(to='social_users.Organisation')),
            ],
        ),
        migrations.RemoveField(
            model_name='membership',
            name='organisation',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='user',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='site',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='trusted_users',
        ),
        migrations.RemoveField(
            model_name='trusteduser',
            name='organizations',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
        migrations.DeleteModel(
            name='Organization',
        ),
        migrations.AddField(
            model_name='organisationsupported',
            name='user',
            field=models.ForeignKey(to='social_users.TrustedUser'),
        ),
        migrations.AddField(
            model_name='organisation',
            name='trusted_users',
            field=models.ManyToManyField(to='social_users.TrustedUser', through='social_users.OrganisationSupported', blank=True),
        ),
        migrations.AddField(
            model_name='trusteduser',
            name='organisations_supported',
            field=models.ManyToManyField(to='social_users.Organisation', through='social_users.OrganisationSupported', blank=True),
        ),
    ]
