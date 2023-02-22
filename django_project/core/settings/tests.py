from .dev import *  # noqa

# -------------------------------------------------- #
# ----------             OSM            ------------ #
# -------------------------------------------------- #
DEV_OSM_API_URL = 'https://api06.dev.openstreetmap.org'
AUTHENTICATION_BACKENDS = (
    'core.backends.dev_openstreetmap.OpenStreetMapDevOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
