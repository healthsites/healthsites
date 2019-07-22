# -*- coding: utf-8 -*-
from __future__ import absolute_import

from celery.utils.log import get_task_logger
from django.utils import timezone

from localities.celery import app
from localities.tasks import regenerate_cache_cluster, send_email
from .importers import CSVtoOSMImporter

logger = get_task_logger(__name__)


@app.task(bind=True)
def upload_data_from_csv(self, data_loader_pk):
    # Put here to avoid circular import
    from localities.models import DataLoader
    try:
        data_loader = DataLoader.objects.get(pk=data_loader_pk)

        # import data from csv to osm
        csv_importer = CSVtoOSMImporter(
            data_loader,
            data_loader.csv_data.path,
            data_loader.json_concept_mapping.path)

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
