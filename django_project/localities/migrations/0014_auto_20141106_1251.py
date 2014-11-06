# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0013_auto_20141106_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='attribute',
            name='changeset',
            field=models.ForeignKey(default=-1, to='localities.Changeset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='domain',
            name='changeset',
            field=models.ForeignKey(default=-1, to='localities.Changeset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='locality',
            name='changeset',
            field=models.ForeignKey(default=-1, to='localities.Changeset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='specification',
            name='changeset',
            field=models.ForeignKey(default=-1, to='localities.Changeset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='value',
            name='changeset',
            field=models.ForeignKey(default=-1, to='localities.Changeset'),
            preserve_default=False,
        ),
    ]
