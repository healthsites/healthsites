# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0011_locality_is_master'),
    ]

    operations = [
        migrations.CreateModel(
            name='SynonymLocalities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locality_id', models.ForeignKey(related_name='master_of_synonym', to='localities.Locality')),
                ('synonym_id', models.ForeignKey(related_name='synonym_of_locality', to='localities.Locality')),
            ],
        ),
        migrations.CreateModel(
            name='UnconfirmedSynonym',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locality_id', models.ForeignKey(related_name='master_of_unconfirmed_synonym', to='localities.Locality')),
                ('synonym_id', models.ForeignKey(related_name='unconfirmed_synonym', to='localities.Locality')),
            ],
        ),
        migrations.AddField(
            model_name='locality',
            name='synonyms',
            field=models.ManyToManyField(related_name='synonyms_list', through='localities.SynonymLocalities', to='localities.Locality'),
        ),
        migrations.AddField(
            model_name='locality',
            name='unconfirmed_synonyms',
            field=models.ManyToManyField(related_name='unconfirmed_synonyms_list', through='localities.UnconfirmedSynonym', to='localities.Locality'),
        ),
    ]
