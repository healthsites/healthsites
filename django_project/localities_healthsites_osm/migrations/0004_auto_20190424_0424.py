# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_healthsites_osm', '0003_auto_20190215_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('value', models.CharField(max_length=512)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterModelOptions(
            name='localityhealthsitesosm',
            options={'ordering': ('osm_id',), 'verbose_name': 'Healthsites And Osm', 'verbose_name_plural': 'Healthsites And Osm'},
        ),
        migrations.RemoveField(
            model_name='localityhealthsitesosm',
            name='healthsite',
        ),
        migrations.AddField(
            model_name='localityhealthsitesosm',
            name='custom_tag',
            field=models.ManyToManyField(to='localities_healthsites_osm.Tag', blank=True),
        ),
    ]
