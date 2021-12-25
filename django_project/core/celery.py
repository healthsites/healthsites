from __future__ import absolute_import

from celery import Celery

app = Celery('project')

app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
