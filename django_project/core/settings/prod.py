# -*- coding: utf-8 -*-
from .project import *

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

if 'raven.contrib.django' in INSTALLED_APPS:
    SENTRY_DSN = ('#REPLACE ME#')

    MIDDLEWARE_CLASSES = (
        'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
        'raven.contrib.django.middleware.SentryLogMiddleware',
    ) + MIDDLEWARE_CLASSES

    #
    # Sentry settings - logs exceptions to a database
    LOGGING = {
        # internal dictConfig version - DON'T CHANGE
        'version': 1,
        'disable_existing_loggers': True,
        # default root logger - handle with sentry
        'root': {
            'level': 'ERROR',
            'handlers': ['sentry'],
        },
        'handlers': {
            # send email to mail_admins, if DEBUG=False
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler'
            },
            # sentry logger
            'sentry': {
                'level': 'WARNING',
                'class': 'raven.contrib.django.handlers.SentryHandler',
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['sentry'],
                'propagate': False
            },
            'raven': {
                'level': 'ERROR',
                'handlers': ['mail_admins'],
                'propagate': False
            },
            'sentry.errors': {
                'level': 'ERROR',
                'handlers': ['mail_admins'],
                'propagate': False
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True
            }
        }
    }
