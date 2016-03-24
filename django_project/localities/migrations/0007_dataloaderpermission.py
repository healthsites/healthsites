# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import localities.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('localities', '0006_auto_20160208_0626'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataLoaderPermission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted_csv', models.FileField(help_text=b'Accepted CSV data that contains the data.', upload_to=b'accepted_csv_data/', verbose_name=b'Accepted CSV Data', validators=[localities.models.validate_file_extension])),
                ('uploader', models.ForeignKey(verbose_name=b'Uploader', to=settings.AUTH_USER_MODEL, help_text=b'The user who propose the data loader.')),
            ],
        ),
    ]
