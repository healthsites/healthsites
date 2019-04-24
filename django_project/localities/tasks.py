# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import datetime

from django.core import management
from django.core.mail import send_mail

from celery import shared_task
from celery.utils.log import get_task_logger

from .celery import app
from .importers import CSVImporter

logger = get_task_logger(__name__)


def send_email(data_loader, report, additional_email=[]):
    """Send email for data loader."""
    logger.info('Send email report.')
    recipient_list = [
        'irwan@kartoza.com',
        'mark@healthsites.io',
    ]
    recipient_list = recipient_list + additional_email

    email_message = 'Loading data for %s\n\n' % data_loader.organisation_name

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


@app.task(bind=True)
def load_data_task(self, data_loader_pk):
    # Put here to avoid circular import
    from .models import DataLoader, DataLoaderPermission
    from django.core.management import call_command
    try:
        data_loader = DataLoader.objects.get(pk=data_loader_pk)
        permissions = DataLoaderPermission.objects.filter(uploader=data_loader.author)
        is_permitted = False
        permission_id = -999
        if not data_loader.author.is_staff:
            try:
                for permission in permissions:
                    with open(data_loader.csv_data.path) as f1:
                        with open(permission.accepted_csv.path) as f2:
                            if f1.read() == f2.read():
                                permission_id = permission.id
                                break
            except Exception as e:
                print e
        else:
            is_permitted = True

        try:
            if not is_permitted:
                permission = DataLoaderPermission.objects.get(id=permission_id)

            csv_importer = CSVImporter(
                data_loader,
                'Health',
                data_loader.organisation_name,
                data_loader.csv_data.path,
                data_loader.json_concept_mapping.path,
                use_tabs=False,
                user=data_loader.author,
                mode=data_loader.data_loader_mode
            )
            logger.info('Finish loading data')

            # update data_loader
            data_loader.applied = True
            data_loader.date_time_applied = datetime.utcnow()
            data_loader.notes = csv_importer.generate_report()
            logger.info('date_time_applied: %s' % data_loader.date_time_applied)
            data_loader.save()

            # send email
            logger.info(csv_importer.generate_report())

            send_email(data_loader, csv_importer.generate_report(), [data_loader.author.email])

            # remove the permission
            if not is_permitted:
                permission.delete()

            call_command('generate_countries_cache')
            regenerate_cache_cluster()
        except DataLoaderPermission.DoesNotExist:
            print 'file is not authenticated'
            logger.info('file is not authenticated')
            send_email(data_loader, 'file is not authenticated', [data_loader.author.email])

    except DataLoader.DoesNotExist as exc:
        raise self.retry(exc=exc, countdown=30, max_retries=5)


@app.task(bind=True)
def regenerate_cache(self, changeset_pk, locality_pk):
    from django.core import management
    from localities.models import Changeset, Country, Locality

    try:
        locality = Locality.objects.get(pk=locality_pk)
        countries = Country.objects.filter(polygon_geometry__contains=locality.geom)
        management.call_command(
            'generate_countries_cache', countries=','.join(
                [country.name for country in countries])
        )
    except Changeset.DoesNotExist as exc:
        raise self.retry(exc=exc, countdown=5, max_retries=10)
    except Locality.DoesNotExist as exc:
        raise self.retry(exc=exc, countdown=5, max_retries=10)
    except Exception as e:
        print e


@app.task(bind=True)
def regenerate_cache_cluster(self):
    from django.core.management import call_command
    call_command('gen_cluster_cache', 48, 46)


@shared_task(name='localities.tasks.generate_shapefile')
def generate_shapefile():
    management.call_command('generate_shapefile_v2')


@app.task(bind=True)
def country_data_into_shapefile_task(self, country):
    from localities.management.commands.generate_shapefile_v2 import (
        country_data_into_shapefile
    )
    country_data_into_shapefile(country)
