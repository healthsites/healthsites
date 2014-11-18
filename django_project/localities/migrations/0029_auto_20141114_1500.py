# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import itertools

from django.db import models, migrations


def prepare_for_fts(locality):
    data_values = itertools.groupby(
        locality.value_set.order_by('specification__fts_rank')
        .values_list('specification__fts_rank', 'data'),
        lambda x: x[0]
    )

    return {k: ' '.join([x[1] for x in v]) for k, v in data_values}


def build_initialftsindex(apps, schema_editor):
    LocalityIndex = apps.get_model('localities', 'LocalityIndex')
    Locality = apps.get_model('localities', 'Locality')

    for loc in Locality.objects.all():
        loc_fts = prepare_for_fts(loc)

        locind = LocalityIndex()
        locind.locality = loc

        locind.ranka = loc_fts.get('A', '')
        locind.rankb = loc_fts.get('B', '')
        locind.rankc = loc_fts.get('C', '')
        locind.rankd = loc_fts.get('D', '')

        locind.save()


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0028_auto_20141114_1500'),
    ]

    operations = [
        migrations.RunPython(build_initialftsindex),
    ]
