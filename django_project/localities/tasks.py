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


def send_email(data_loader, csv_importer):
    """Send email for data loader."""
    logger.info('Send email report.')
    recipient_list = [
        'ismail@kartoza.com',
        'mark.herringer@gmail.com'
    ]

    email_message = 'Loading data for %s\n\n' % data_loader.organisation_name

    email_message += 'Details:\n'
    email_message += 'Uploader %s\n' % data_loader.author
    email_message += 'Data Loading mode %s\n' % data_loader.get_data_loader_mode_display()
    email_message += 'Uploaded on %s\n' % data_loader.date_time_uploaded
    email_message += 'Finished loading on %s\n\n' % data_loader.date_time_applied

    email_message += csv_importer.generate_report() + '\n\n'

    email_message += "You receive this email because you are the admin of Healthsites.io"

    send_mail(
        subject='Healthsites Data Loader Report',
        message=email_message,
        from_email='dataloader@healthsites.io',
        recipient_list=recipient_list,
        fail_silently=False,
    )


@app.task
def load_data_task(data_loader_pk):
    # Put here to avoid circular import
    from .models import DataLoader

    data_loader = DataLoader.objects.get(pk=data_loader_pk)
    logger.info('Start loading data')
    # Process data
    csv_importer = CSVImporter(
        'Health',
        data_loader.organisation_name,
        data_loader.csv_data.path,
        data_loader.json_concept_mapping.path,
        use_tabs=False,
        user=data_loader.author,
        mode=data_loader.data_loader_mode
    )
    logger.info('Finish loading data')

    # send email
    logger.info(csv_importer.generate_report())

    send_email(data_loader, csv_importer)

    # update data_loader
    data_loader.applied = True
    data_loader.date_time_applied = datetime.utcnow()
    data_loader.notes = csv_importer.generate_report()
    logger.info('date_time_applied: %s' % data_loader.date_time_applied)
    data_loader.save()


@app.task
def test_task(x, y):
    logger.info('Load data')
    print x + y