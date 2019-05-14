from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    'generate-cluster': {
        'task': 'localities.tasks.regenerate_cache_cluster',
        'schedule': 3600.0,
    },
}

CELERY_TIMEZONE = 'UTC'
