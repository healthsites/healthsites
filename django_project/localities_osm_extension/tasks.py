# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '15/05/19'

from localities.celery import app
from django.core import management


@app.task(name='localities.tasks.migrate_old_data')
def migrate_old_data(username):
    management.call_command(
        'migrate_old_data', username=username)
