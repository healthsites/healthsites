# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import pg_fts.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('key', models.TextField(unique=True)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AttributeArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('key', models.TextField()),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Changeset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField()),
                ('comment', models.TextField(null=True, blank=True)),
                ('social_user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataLoader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('organisation_name', models.CharField(help_text=b"Organization's Name", max_length=100, verbose_name=b"Organization's Name")),
                ('json_concept_mapping', models.FileField(help_text=b'JSON Concept Mapping File.', upload_to=b'json_mapping/%Y/%m/%d', verbose_name=b'JSON Concept Mapping')),
                ('csv_data', models.FileField(help_text=b'CSV data that contains the data.', upload_to=b'csv_data/%Y/%m/%d', verbose_name=b'CSV Data')),
                ('data_loader_mode', models.IntegerField(help_text=b'The mode of the data loader.', verbose_name=b'Data Loader Mode', choices=[(1, b'Replace Data'), (2, b'Update Data')])),
                ('applied', models.BooleanField(default=False, help_text=b'Whether the data update has been applied or not.', verbose_name=b'Applied')),
                ('date_time_uploaded', models.DateTimeField(help_text=b'Timestamp (UTC) when the data uploaded', verbose_name=b'Uploaded (time)')),
                ('date_time_applied', models.DateTimeField(help_text=b'When the data applied (loaded)', null=True, verbose_name=b'Applied (time)')),
                ('separator', models.IntegerField(default=1, help_text=b'Separator character.', verbose_name=b'Separator Character', choices=[(1, b'Comma'), (2, b'Tab')])),
                ('notes', models.TextField(default=b'', help_text=b'Notes', null=True, verbose_name=b'Notes', blank=True)),
                ('author', models.ForeignKey(verbose_name=b'Author', to=settings.AUTH_USER_MODEL, help_text=b'The user who propose the data loader.')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(default=b'', null=True, blank=True)),
                ('template_fragment', models.TextField(default=b'', null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DomainArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
                ('template_fragment', models.TextField(null=True, blank=True)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Locality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('uuid', models.TextField(unique=True)),
                ('upstream_id', models.TextField(unique=True, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('domain', models.ForeignKey(to='localities.Domain')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalityArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('domain_id', models.IntegerField()),
                ('uuid', models.TextField()),
                ('upstream_id', models.TextField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LocalityIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ranka', models.TextField(null=True)),
                ('rankb', models.TextField(null=True)),
                ('rankc', models.TextField(null=True)),
                ('rankd', models.TextField(null=True)),
                ('fts_index', pg_fts.fields.TSVectorField(dictionary='english', default='', fields=((b'ranka', b'A'), (b'rankb', b'B'), (b'rankc', b'C'), (b'rankd', b'D')), serialize=False, editable=False, null=True)),
                ('locality', models.OneToOneField(to='localities.Locality')),
            ],
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('required', models.BooleanField(default=False)),
                ('fts_rank', models.CharField(default=b'D', max_length=1, choices=[(b'A', b'Rank A'), (b'B', b'Rank B'), (b'C', b'Rank C'), (b'D', b'Rank D')])),
                ('attribute', models.ForeignKey(to='localities.Attribute')),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('domain', models.ForeignKey(to='localities.Domain')),
            ],
        ),
        migrations.CreateModel(
            name='SpecificationArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('domain_id', models.IntegerField()),
                ('attribute_id', models.IntegerField()),
                ('required', models.BooleanField(default=False)),
                ('fts_rank', models.CharField(max_length=1)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('data', models.TextField(blank=True)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('locality', models.ForeignKey(to='localities.Locality')),
                ('specification', models.ForeignKey(to='localities.Specification')),
            ],
        ),
        migrations.CreateModel(
            name='ValueArchive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField()),
                ('object_id', models.IntegerField()),
                ('locality_id', models.IntegerField()),
                ('specification_id', models.IntegerField()),
                ('data', models.TextField(blank=True)),
                ('changeset', models.ForeignKey(to='localities.Changeset')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='locality',
            name='specifications',
            field=models.ManyToManyField(to='localities.Specification', through='localities.Value'),
        ),
        migrations.AddField(
            model_name='domain',
            name='attributes',
            field=models.ManyToManyField(to='localities.Attribute', through='localities.Specification'),
        ),
        migrations.AddField(
            model_name='domain',
            name='changeset',
            field=models.ForeignKey(to='localities.Changeset'),
        ),
        migrations.AddField(
            model_name='attributearchive',
            name='changeset',
            field=models.ForeignKey(to='localities.Changeset'),
        ),
        migrations.AddField(
            model_name='attributearchive',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='attribute',
            name='changeset',
            field=models.ForeignKey(to='localities.Changeset'),
        ),
        migrations.AlterUniqueTogether(
            name='value',
            unique_together=set([('locality', 'specification')]),
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together=set([('domain', 'attribute')]),
        ),
    ]
