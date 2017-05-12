# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf import settings

from celery import Celery

app = Celery('localities')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
