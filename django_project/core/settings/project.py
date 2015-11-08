# -*- coding: utf-8 -*-
from .contrib import *  # noqa

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # Or path to database file if using sqlite3.
        'NAME': '',
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': '',
        # Set to empty string for default.
        'PORT': '',
    }
}

# Project apps
INSTALLED_APPS += (
    'localities',
    'frontend',
    'social_users',
    'api'
)

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/signin/'

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.NoopCompressor'

PIPELINE_JS = {
    'contrib': {
        'source_filenames': (
            'js/leaflet.js',
            'js/leaflet.draw-src.js',
            'js/jquery-1.11.3.min.js',
            'js/bootstrap.min.js',
            'js/d3.min.js',
            'js/c3.min.js',
            'js/rhinoslider-1.05.min.js',
        ),
        'output_filename': 'js/contrib.js',
    },
    'appjs': {
        'source_filenames': (
            'js/clusterLayer.js',
            'js/csrf-ajax.js',
            'js/app.js',
            'js/map.js',
            'js/localitySidebar.js'
        ),
        'output_filename': 'js/appjs.js'
    },
    'home': {
        'source_filenames': (
            'js/jquery-ui.js',
            'js/custom-jquery.js',
        ),
        'output_filename': 'js/home.js',
    },
    'map': {
        'source_filenames': (
            'js/custom-jquery.js',
        ),
        'output_filename': 'js/map.js',
    },
}

PIPELINE_CSS = {
    'contrib': {
        'source_filenames': (
            'css/leaflet.css',
            'css/leaflet.draw.css',
            'css/bootstrap.min.css',
            'css/font-awesome.min.css',
            'css/c3.css',
        ),
        'output_filename': 'css/contrib.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    },
    'home': {
        'source_filenames': (
            'css/jquery-ui.css',
            'css/site.css',
            'css/home.css',
        ),
        'output_filename': 'css/home.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    },
    'map': {
        'source_filenames': (
            'css/site.css',
            'css/map.css',
        ),
        'output_filename': 'css/map.css',
        'extra_context': {
            'media': 'screen, projection',
        },
    },
}
