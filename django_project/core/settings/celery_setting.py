from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'generate-shapefile': {
        'task': 'localities.tasks.generate_shapefile',
        'schedule': crontab(hour=23, minute=59),
    },
}

CELERY_TIMEZONE = 'UTC'
