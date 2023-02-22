# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomFlatPage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage', on_delete=django.db.models.deletion.CASCADE)),
                ('enrollment_title', models.CharField(unique=True, max_length=200)),
                ('gather_url', models.CharField(max_length=250)),
                ('gather_username', models.CharField(max_length=250)),
                ('gather_password', models.CharField(max_length=250)),
            ],
            bases=('flatpages.flatpage',),
        ),
    ]
