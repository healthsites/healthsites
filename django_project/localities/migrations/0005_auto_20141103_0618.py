# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0004_auto_20141031_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('required', models.BooleanField(default=False)),
                ('attribute', models.ForeignKey(to='localities.Attribute')),
                ('domain', models.ForeignKey(to='localities.Domain')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together=set([('domain', 'attribute')]),
        ),
        migrations.AddField(
            model_name='domain',
            name='attributes',
            field=models.ManyToManyField(to='localities.Attribute', through='localities.Specification'),
            preserve_default=True,
        ),
    ]
