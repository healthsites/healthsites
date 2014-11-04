# -*- coding: utf-8 -*-
from .base import *  # noqa

# Extra installed apps
INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'pipeline',
    'social.apps.django_app.default',
)

# define template function (example for underscore)
# PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'


AUTHENTICATION_BACKENDS = (
    'social.backends.openstreetmap.OpenStreetMapOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_OPENSTREETMAP_KEY = 'jDdNNwcqojKUcGVNxXSlpKwTi6q1LH24rKxUHnoY'
SOCIAL_AUTH_OPENSTREETMAP_SECRET = 'AS2nYDWEryS0H2mPS7gHqW2dCnAJyUYOghWUWCDu'

SOCIAL_AUTH_TWITTER_KEY = 'fMUAWDOUFR7Bj18yArV5xFtGA'
SOCIAL_AUTH_TWITTER_SECRET = 'qWpWIpYUBpN73WbwZYF25p2quHleHwNxmZ5Ss1Y7ryzqYtviwC'

SOCIAL_AUTH_GITHUB_KEY = '80bd823edf9b37bc1faa'
SOCIAL_AUTH_GITHUB_SECRET = '5044e80411289a89bcfc41dd30c70cb2abd9917a'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '118859538322-cvdq0g5pev88oigsjmpvndlek1j7q9t5.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'a7v3QY19iu3D_uP2TYBW14Zv'

SOCIAL_AUTH_FACEBOOK_KEY = '739607739442410'
SOCIAL_AUTH_FACEBOOK_SECRET = '8b2886bea4ee73ad698f22e57514abcd'
