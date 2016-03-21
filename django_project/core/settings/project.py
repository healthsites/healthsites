# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa
from django.utils.translation import ugettext_lazy as _
from .utils import absolute_path
from .contrib import *  # noqa
from .secret import *  # secret

# Project apps
INSTALLED_APPS += (
    'localities',
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
LOCALE_PATHS = (absolute_path('locale'),)

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
# Maybe we can split these between project-home and project-map
PIPELINE_JS['home'] = {
    'source_filenames': (
        'js/index-page.js',
    ),
    'output_filename': 'js/home.js',
}
PIPELINE_JS['map.js'] = {
    'source_filenames': (
        'js/map-page.js',
    ),
    'output_filename': 'js/map.js.js',
}

PIPELINE_JS['project'] = {
    'source_filenames': (
        'js/utilities.js',
        'js/custom-functions.js',
        'js/cookie-bar.js',
        'js/custom-jquery.js',
        'js/csrf-ajax.js',
        'js/nav-bar.js',
    ),
    'output_filename': 'js/project.js',
}
PIPELINE_JS['map'] = {
    'source_filenames': (
        'js/cluster-layer.js',
        'js/locality-sidebar.js',
        'js/map-functionality.js',
        'js/_app.js',
        'js/google-analytics.js',
    ),
    'output_filename': 'js/map.js',
}

# Contributed / third party css for pipeline compression
# For hand rolled css for this app, use project.py
PIPELINE_CSS['project'] = {
    'source_filenames': (
        'css/site.css',
        'css/profile.css',
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
CLUSTER_CACHE_DIR = 'cache'
