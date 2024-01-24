# Generated by Django 3.2.18 on 2023-07-03 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SitePreferences',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_max_request_api', models.IntegerField(default=50, help_text='Default max request per day for api key.')),
                ('site_url', models.CharField(blank=True, help_text='Site url that will be used for code.', max_length=32, null=True)),
            ],
            options={
                'verbose_name_plural': 'site preferences',
            },
        ),
    ]
