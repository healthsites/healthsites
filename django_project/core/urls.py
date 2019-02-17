# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns(
    '',

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # uncomment to enable defaut Django auth
    # url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # include application urls
    url(r'', include('frontend.urls')),
    url(r'', include('localities.urls')),
    url(r'', include('social_users.urls')),
    url(r'api/', include('api.urls')),

)

# expose static files and uploded media if DEBUG is active
urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True
        }),
    url(r'', include('django.contrib.staticfiles.urls'))
)
