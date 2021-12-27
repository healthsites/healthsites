from __future__ import absolute_import

from celery import Celery

app = Celery('project')

app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'run-harvester': {
        'task': 'localities.tasks.run_generate_osm_administrative_code',
        'schedule': 60 * 60 * 1,
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
