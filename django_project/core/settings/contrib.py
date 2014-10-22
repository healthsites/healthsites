from .base import *

# Extra installed apps
INSTALLED_APPS += (
    # 'raven.contrib.django',  # enable Raven plugin
    'pipeline',
)

# define template function (example for underscore)
# PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
