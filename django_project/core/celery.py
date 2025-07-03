from __future__ import absolute_import

from celery.schedules import crontab

from celery import Celery

app = Celery('project')

app.config_from_object('django.conf:settings', namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-osm-administrative-code': {
        'task': 'localities.tasks.run_generate_osm_administrative_code',
        'schedule': 60 * 60 * 1,
    },
    'regenerate-cluster-cache': {
        'task': 'localities.tasks.regenerate_cache_cluster',
        'schedule': crontab(minute=0, hour=22),
    },
    'regenerate-shapefile': {
        'task': 'localities.tasks.generate_shapefile',
        'schedule': crontab(minute=0, hour=2),
    },
    'generate-statistic-countries': {
        'task': 'localities.tasks.generate_statistic_countries',
        'schedule': crontab(minute=0),
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
