# coding=utf-8

"""Project level settings."""
from .prod_docker import *  # noqa

OSM_API_URL = 'https://upload.apis.dev.openstreetmap.org'
try:
    SOCIAL_AUTH_OPENSTREETMAP_KEY = SOCIAL_AUTH_OPENSTREETMAP_STAGING_KEY
    SOCIAL_AUTH_OPENSTREETMAP_SECRET = SOCIAL_AUTH_OPENSTREETMAP_STAGING_SECRET
except ImportError:
    pass

AUTHENTICATION_BACKENDS = (
    'core.backends.dev_openstreetmap.OpenStreetMapDevOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
