# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url

from .views import AboutView, AttributionsView, MainView, MessagesContactView

urlpatterns = patterns(
    '',
    # basic app views
    url(r'^$', MainView.as_view(), name='home'),
    url(r'^contact/', MessagesContactView.as_view(), name='envelope-contact'),
    url(r'^about$', AboutView.as_view(), name='about'),
    url(r'^map$', 'frontend.views.map', name='map'),
    url(r'^attributions$', AttributionsView.as_view(), name='attribution'),
)
