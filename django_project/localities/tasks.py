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


from celery.utils.log import get_task_logger
from .celery import app

logger = get_task_logger(__name__)

from .importers import CSVImporter


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