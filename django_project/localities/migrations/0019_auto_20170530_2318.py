# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities', '0018_auto_20160609_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataloaderpermission',
            name='uploader',
            field=models.ForeignKey(verbose_name=b'Uploader', to='social_users.TrustedUser', help_text=b'The user who propose the data loader.'),
        ),
        migrations.RunSQL(
          "update localities_dataloaderpermission set uploader_id=subq.id from (select id, user_id from social_users_trustedusers) as subq where localities_dataloaderpermission.uploader_id = subq.user_id"
        ),
    ]
