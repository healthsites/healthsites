# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os

from django.core import management
from django.core.mail import send_mail
from django.utils import timezone
from celery.utils.log import get_task_logger

from api.importers import CSVtoOSMImporter
from core.celery import app

logger = get_task_logger(__name__)


def send_email(data_loader, report, additional_email=[]):
    """Send email for data loader."""
    logger.info('Send email report.')
    recipient_list = [
        'irwan@kartoza.com',
        'mark@healthsites.io',
    ]
    recipient_list = recipient_list + additional_email

    email_message = 'Loading data\n\n'

    email_message += 'Details:\n'
    email_message += 'Uploader: %s\n' % data_loader.author
    email_message += 'Data Loading mode: %s\n' % data_loader.get_data_loader_mode_display()
    email_message += 'Uploaded on: %s\n' % data_loader.date_time_uploaded
    email_message += 'Finished loading on: %s\n\n' % data_loader.date_time_applied

    email_message += report + '\n\n'

    email_message += 'You receive this email because you are the admin of Healthsites.io'

    send_mail(
        subject='Healthsites Data Loader Report',
        message=email_message,
        from_email='dataloader@healthsites.io',
        recipient_list=recipient_list,
        fail_silently=False,
    )


@app.task
def generate_shapefile():
    management.call_command('generate_shapefile_countries')


@app.task
def regenerate_cache_cluster():
    from django.core.management import call_command
    call_command('generate_cluster_cache')


@app.task
def country_data_into_shapefile_task(country):
    from api.management.commands.generate_shapefile_countries import (
        country_data_into_shapefile,
        get_shapefile_folder
    )
    country_cache = get_shapefile_folder(country)
    metadata_file = os.path.join(country_cache, 'metadata')
    try:
        f = open(metadata_file, 'r')
        file_content = f.read()
        if file_content == 'Start':
            return False
    except IOError:
        if not os.path.exists(country_cache):
            os.makedirs(country_cache)
        file = open(metadata_file, 'w+')
        file.write('Start')
        file.close()

    try:
        country_data_into_shapefile(country)
        try:
            os.remove(metadata_file)
        except OSError:
            pass
    except Exception as e:
        try:
            os.remove(metadata_file)
        except OSError:
            pass
        raise e


@app.task
def country_data_into_statistic_task(extent, country):
    from django.core.management import call_command
    if not extent:
        extent = ''
    if not country:
        country = ''
    call_command('generate_statistic_country', extent=extent, country=country)


@app.task(bind=True, max_retries=3)
def upload_data_from_csv(self, data_loader_pk):
    # Put here to avoid circular import
    from localities.models import DataLoader
    try:
        data_loader = DataLoader.objects.get(pk=data_loader_pk)

        # import data from csv to osm
        csv_importer = CSVtoOSMImporter(
            data_loader,
            data_loader.csv_data.path)

        # update data_loader
        DataLoader.objects.filter(pk=data_loader_pk).update(
            applied=csv_importer.is_applied(),
            date_time_applied=timezone.now(),
            notes=csv_importer.generate_report())

        # update data_loader reference
        data_loader = DataLoader.objects.get(pk=data_loader_pk)
        logger.info('date_time_applied: %s' % data_loader.date_time_applied)

        # send email
        logger.info(csv_importer.generate_report())
        send_email(
            data_loader, csv_importer.generate_report(),
            [data_loader.author.email])

    except DataLoader.DoesNotExist as exc:
        raise self.retry(exc=exc, countdown=30, max_retries=5)


@app.task
def run_generate_osm_administrative_code():
    management.call_command('generate_osm_administrative_code')
