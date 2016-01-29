# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localities', '0003_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_changed', models.DateTimeField(default=None, help_text=b'Timestamp (UTC) when the data uploaded', verbose_name=b'Uploaded (time)')),
                ('mode', models.IntegerField(default=1, help_text=b'The mode of the data loader.', verbose_name=b'Data Loader Mode', choices=[(1, b'Replace Data'), (2, b'Update Data')])),
                ('author', models.ForeignKey(default=None, verbose_name=b'Author', to=settings.AUTH_USER_MODEL, help_text=b'The user who edit or add data')),
                ('locality', models.ForeignKey(to='localities.Locality')),
            ],
        ),
    ]
