# coding=utf-8
"""Docstring for this file."""
from __future__ import absolute_import

__author__ = 'ismailsunni'
__project_name = 'healthsites'
__filename = 'tasks'
__date__ = '8/27/15'
__copyright__ = 'imajimatika@gmail.com'
__doc__ = ''


from celery import shared_task
from celery.utils.log import get_task_logger
from .celery import app

from django.core.mail import send_mail

logger = get_task_logger(__name__)

from .importers import CSVImporter


@app.task
def load_data_task(data_loader_pk):
    from .models import DataLoader

    data_loader = DataLoader.objects.get(pk=data_loader_pk)
    logger.info('Load data')
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

    # send email
    # update data_loader
    data_loader.applied = True
    data_loader.save()


@app.task
def test_task(x, y):
    logger.info('Load data')
    print x + y