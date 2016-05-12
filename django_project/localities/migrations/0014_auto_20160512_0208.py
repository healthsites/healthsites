# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0013_auto_20160510_0423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='synonymlocalities',
            options={'ordering': ['locality', 'synonym'], 'verbose_name': 'Synonyms', 'verbose_name_plural': 'Synonyms'},
        ),
        migrations.AlterModelOptions(
            name='unconfirmedsynonym',
            options={'ordering': ['locality', 'synonym'], 'verbose_name': 'Potential Synonym', 'verbose_name_plural': 'Potential Synonyms'},
        ),
    ]
