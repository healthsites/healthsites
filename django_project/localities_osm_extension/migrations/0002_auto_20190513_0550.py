# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('localities_osm_extension', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='localityosmextension',
            name='custom_tag',
        ),
        migrations.RemoveField(
            model_name='localityosmextension',
            name='osm_pk',
        ),
        migrations.AddField(
            model_name='tag',
            name='extension',
            field=models.ForeignKey(default=None, to='localities_osm_extension.LocalityOSMExtension', on_delete=django.db.models.deletion.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('extension', 'name')]),
        ),
    ]
