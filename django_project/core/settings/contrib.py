# -*- coding: utf-8 -*-
from .base import *  # noqa

# Extra installed apps
INSTALLED_APPS += (
    'pipeline',
    'social.apps.django_app.default',
    'pg_fts',
)

# define template function (example for underscore)
# PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'


STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder'
)

AUTHENTICATION_BACKENDS = (
    'social.backends.openstreetmap.OpenStreetMapOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
