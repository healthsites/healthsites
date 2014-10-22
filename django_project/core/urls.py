from django.conf.urls import patterns, include, url
from django.conf import settings

from django.contrib import admin


urlpatterns = patterns(
    '',

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # uncomment to enable defaut Django auth
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # include application urls
    # url(r'', include('application.urls')),

)

# expose static files and uploded media if DEBUG is active
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {
                'document_root': settings.MEDIA_ROOT,
                'show_indexes': True
            }),
        url(r'', include('django.contrib.staticfiles.urls')),
    )
