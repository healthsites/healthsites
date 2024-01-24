# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('flatpages', '0001_initial'),
        ('social_users', '0010_auto_20190712_0831'),
        ('frontend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CampaignPage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage', on_delete=django.db.models.deletion.CASCADE)),
                ('campaign_title', models.CharField(unique=True, max_length=200)),
                ('gather_url', models.CharField(max_length=250)),
                ('organisation', models.ForeignKey(to='social_users.Organisation', on_delete=django.db.models.deletion.CASCADE)),
            ],
            options={
                'verbose_name': 'Campaign Page',
                'verbose_name_plural': 'Campaign Pages',
            },
            bases=('flatpages.flatpage',),
        ),
        migrations.RemoveField(
            model_name='customflatpage',
            name='flatpage_ptr',
        ),
        migrations.DeleteModel(
            name='CustomFlatPage',
        ),
    ]
