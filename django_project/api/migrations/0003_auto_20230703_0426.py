# Generated by Django 3.2.18 on 2023-07-03 04:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_userapikey_allow_write'),
    ]

    operations = [
        migrations.AddField(
            model_name='userapikey',
            name='max_request_per_day',
            field=models.IntegerField(blank=True, help_text='Maximum allowed API requests per day for the API key. If empty, it will use the default_max_request_api preference.', null=True),
        ),
        migrations.AlterField(
            model_name='userapikey',
            name='allow_write',
            field=models.BooleanField(default=False, help_text='Allow this API key to write data.'),
        ),
        migrations.AlterField(
            model_name='userapikey',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ApiKeyRequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=126)),
                ('time', models.DateTimeField()),
                ('url', models.TextField()),
                ('api_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userapikey')),
            ],
        ),
        migrations.CreateModel(
            name='ApiKeyEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_person', models.CharField(max_length=512)),
                ('contact_email', models.EmailField(max_length=254)),
                ('organisation_name', models.CharField(max_length=512)),
                ('organisation_url', models.CharField(max_length=512, validators=[django.core.validators.URLValidator()])),
                ('project_url', models.CharField(help_text='Web site or project URL for which the Healthsites API will be used.', max_length=512, validators=[django.core.validators.URLValidator()])),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False, help_text='When approved, the api_key will be created and activated')),
                ('api_key', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.userapikey')),
            ],
        ),
        migrations.CreateModel(
            name='ApiKeyAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('counter', models.IntegerField(default=0)),
                ('api_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userapikey')),
            ],
        ),
    ]