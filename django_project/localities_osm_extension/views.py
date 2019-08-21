# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '15/05/19'

from django.http import HttpResponse
from .tasks import migrate_old_data


def execute_migration(request, username):
    migrate_old_data.delay(username)
    return HttpResponse('Data migration is started')
