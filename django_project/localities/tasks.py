# coding=utf-8
"""Docstring for this file."""
from __future__ import absolute_import

__author__ = 'ismailsunni'
__project_name = 'healthsites'
__filename = 'tasks'
__date__ = '8/27/15'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''

from datetime import datetime

from django.core.mail import send_mail

from celery.utils.log import get_task_logger
from .celery import app

logger = get_task_logger(__name__)

from .importers import CSVImporter


def send_email(data_loader, report):
    """Send email for data loader."""
    logger.info('Send email report.')
    recipient_list = [
        'ismail@kartoza.com',
        'mark.herringer@gmail.com'
    ]

    email_message = 'Loading data for %s\n\n' % data_loader.organisation_name

    email_message += 'Details:\n'
    email_message += 'Uploader: %s\n' % data_loader.author
    email_message += 'Data Loading mode: %s\n' % data_loader.get_data_loader_mode_display()
    email_message += 'Uploaded on: %s\n' % data_loader.date_time_uploaded
    email_message += 'Finished loading on: %s\n\n' % data_loader.date_time_applied

    email_message += report + '\n\n'

    email_message += "You receive this email because you are the admin of Healthsites.io"

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
        permission_id = -999
        try:
            for permission in permissions:
                with open(data_loader.csv_data.path) as f1:
                    with open(permission.accepted_csv.path) as f2:
                        if f1.read() == f2.read():
                            permission_id = permission.id
                            break

        except Exception as e:
            print e

        try:
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

            send_email(data_loader, csv_importer.generate_report())

            # remove the permission
            permission.delete()
            
            call_command('generate_countries_cache')
            regenerate_cache_cluster()
        except DataLoaderPermission.DoesNotExist:
            print "file is not authenticated"
            logger.info("file is not authenticated")
            send_email(data_loader, "file is not authenticated")

    except DataLoader.DoesNotExist as exc:
        raise self.retry(exc=exc, countdown=30, max_retries=5)


@app.task(bind=True)
def regenerate_cache(self, changeset_pk, locality_pk):
    # Put here to avoid circular import
    from .models import Changeset
    from .models import Locality
    from localities.models import Country
    import os
    import json
    from django.conf import settings
    from localities.utils import get_statistic
    from django.core.serializers.json import DjangoJSONEncoder

    try:
        changeset = Changeset.objects.get(pk=changeset_pk)
        locality = Locality.objects.get(pk=locality_pk)
        country = Country.objects.filter(polygon_geometry__contains=locality.geom)

        # write world cache
        filename = os.path.join(
            settings.CLUSTER_CACHE_DIR,
            'world_statistic')
        healthsites = Locality.objects.all()
        output = get_statistic(healthsites)
        result = json.dumps(output, cls=DjangoJSONEncoder)
        file = open(filename, 'w')
        file.write(result)  # python will convert \n to os.linesep
        file.close()  # you can omit in most cases as the destructor will call it

        # getting country's polygon
        if len(country):
            country = country[0]
            polygons = country.polygon_geometry

            # write country cache
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                country.name + '_statistic'
            )
            healthsites = Locality.objects.in_polygon(
                    polygons)
            output = get_statistic(healthsites)
            result = json.dumps(output, cls=DjangoJSONEncoder)
            file = open(filename, 'w')
            file.write(result)  # python will convert \n to os.linesep
            file.close()  # you can omit in most cases as the destructor will call it

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
