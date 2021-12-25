# coding=utf-8
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/08/21'

"""Project level url handler."""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from core.views.template import HomeView

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'', include('frontend.urls')),
    url(r'', include('localities.urls')),
    url(r'', include('social_users.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^$', HomeView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
