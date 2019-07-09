# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os
from django.utils.translation import ugettext_lazy as _

from .celery_setting import *
from .contrib import *  # noqa
from .secret import *  # NOQA

# Project apps
INSTALLED_APPS += (
    'localities',
    'localities_osm',
    'localities_osm_extension',
    'frontend',
    'social_users',
    'api',
    'django_hashedfilenamestorage',
    'envelope'
)

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
    ('af', _('Afrikaans')),
    ('id', _('Indonesian')),
    ('ko', _('Korean')),
)

# Set storage path for the translation files
LOCALE_PATHS = [ABS_PATH('locale')]

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
# Maybe we can split these between project-home and project-map
PIPELINE_JS['home'] = {
    'source_filenames': (
        # this is new using require
        'libs/require.js/2.3.6/require.min.js',
        'scripts/configs/index.js'
    ),
    'output_filename': 'js/home.js',
}
PIPELINE_JS['map.js'] = {
    'source_filenames': (
        'libs/require.js/2.3.6/require.min.js',
        'scripts/configs/map.js'
    ),
    'output_filename': 'js/map.js',
}

PIPELINE_JS['project'] = {
    'source_filenames': (
        'js/utilities.js',
        'js/custom-functions.js',
        'js/cookie-bar.js',
        'js/custom-jquery.js',
        'js/csrf-ajax.js',
        'js/nav-bar.js',
        'js/google-analytics.js',
    ),
    'output_filename': 'js/project.js',
}
PIPELINE_JS['map'] = {
    'source_filenames': (
        'js/locality-sidebar.js',
    ),
    'output_filename': 'js/map.js',
}

# Contributed / third party css for pipeline compression
# For hand rolled css for this app, use project.py
PIPELINE_CSS['project'] = {
    'source_filenames': (
        'css/site.css',
        'css/profile.css',
        'css/map/locality-sidebar.css',
        'css/jquery.cookiebar.css'
    ),
    'output_filename': 'css/project.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}

PIPELINE_CSS['map'] = {
    'source_filenames': (
        'css/map.css',
    ),
    'output_filename': 'css/map.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}
PIPELINE_CSS['home'] = {
    'source_filenames': (
        'css/home.css',
    ),
    'output_filename': 'css/home.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}

# Cache folder
CACHE_DIR = '/home/web/cache'
CLUSTER_CACHE_DIR = os.path.join(CACHE_DIR, 'cluster')
STATISTIC_CACHE_DIR = os.path.join(CACHE_DIR, 'statistic')
CLUSTER_CACHE_MAX_ZOOM = 5
MAX_ZOOM = 18

# WHAT3WORDS API
WHAT3WORDS_API_POS_TO_WORDS = 'https://api.what3words.com/position?key=%s&lang=en&position=%s,%s'
DATABASE_ROUTERS = ['core.router.HealthsiteRouter']
