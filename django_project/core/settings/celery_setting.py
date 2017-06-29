import os

from celery.schedules import crontab

BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'generate-shapefile': {
        'task': 'localities.tasks.generate_shapefile',
        'schedule': crontab(hour=23, minute=59),
    },
}

CELERY_TIMEZONE = 'UTC'
