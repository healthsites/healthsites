# coding=utf-8
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/08/21'

"""Project level url handler."""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.views.generic import View

from core.models.preferences import SitePreferences
from core.views.template import HomeView

admin.autodiscover()


class SitePreferenceAdmin(View):
    """Redirect it to site preference."""

    def get(self, request, **kwargs):
        preference = SitePreferences.preferences()
        return redirect(
            f'/admin/core/sitepreferences/{preference.id}/change/'
        )


urlpatterns = [
    url(r'^admin/core/sitepreferences/$', SitePreferenceAdmin.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'', include('frontend.urls')),
    url(r'', include('localities.urls')),
    url(r'', include('social_users.urls')),
    url(r'', include('api.urls')),
    url(r'^$', HomeView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
