# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa

from django.utils.translation import ugettext_lazy as _

from .contrib import *  # noqa

VERSION = os.environ.get('VERSION', '')
APP_NAME = 'Healthsites.io'
ALLOWED_HOSTS = ['*']
ADMINS = (
    ('Irwan Fathurrahman', 'irwan@kartoza.com'),
)
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_NAME', 'gis'),
        'USER': os.environ.get('DATABASE_USERNAME', 'docker'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'docker'),
        'HOST': os.environ.get('DATABASE_HOST', 'db'),
        'PORT': os.environ.get('DATABASE_PORT', 5432),
        'TEST_NAME': 'unittests',
    },
    'docker_osm': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ.get('DATABASE_OSM_NAME', 'gis'),
        'USER': os.environ.get('DATABASE_OSM_USERNAME', 'osm_docker'),
        'PASSWORD': os.environ.get('DATABASE_OSM_PASSWORD', 'osm_docker'),
        'HOST': os.environ.get('DATABASE_OSM_HOST', 'osm-db'),
        'PORT': os.environ.get('DATABASE_OSM_PORT', 5432),
        'TEST_NAME': 'docker_osm_unittests',
    }
}
DATABASE_ROUTERS = ['core.router.HealthsiteRouter']

# -------------------------------------------------- #
# ----------            CELERY          ------------ #
# -------------------------------------------------- #
CELERY_BROKER_URL = 'amqp://guest:guest@%s:5672//' % os.environ.get(
    'RABBITMQ_HOST', 'rabbitmq')
CELERY_RESULT_BACKEND = None
CELERY_TASK_ALWAYS_EAGER = False  # set this to False in order to run async
CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_DEFAULT_EXCHANGE = "default"
CELERY_TASK_DEFAULT_EXCHANGE_TYPE = "direct"
CELERY_TASK_DEFAULT_ROUTING_KEY = "default"
CELERY_TASK_CREATE_MISSING_QUEUES = True
CELERY_TASK_RESULT_EXPIRES = 1
CELERY_WORKER_DISABLE_RATE_LIMITS = True
CELERY_WORKER_SEND_TASK_EVENTS = False

# Due to profile page does not available,
# this will redirect to home page after login
LOGIN_REDIRECT_URL = '/'

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
)

# Set storage path for the translation files
LOCALE_PATHS = (ABS_PATH('locale'),)

# Extra installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    'core',
    'frontend',
    'localities',
    'localities_osm',
    'localities_osm_extension',
    'healthsites',
    'api',
    'social_users'
)

# DATA LICENSE
LICENSES = [
    ABS_PATH('api', 'LICENSE.txt'),
    ABS_PATH('api', 'README.md')
]

# Cache folder
CACHE_DIR = '/home/web/cache'
CLUSTER_CACHE_DIR = os.path.join(CACHE_DIR, 'cluster')
STATISTIC_CACHE_DIR = os.path.join(CACHE_DIR, 'statistic')
SHAPEFILE_DIR = os.path.join(MEDIA_ROOT, 'shapefiles')
CLUSTER_CACHE_MAX_ZOOM = 8
MAX_ZOOM = 18

# test users will send the data to osm instead just raise error
# fill with username in list
TEST_USERS = os.environ.get('TEST_USERS', '').split(',')

# -------------------------------------------------- #
# ----------             OSM            ------------ #
# -------------------------------------------------- #
DUPLICATION_RADIUS = 100  # in meters
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
