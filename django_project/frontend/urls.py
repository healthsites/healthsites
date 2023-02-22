# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import (
    AboutView, AttributionsView, HelpView, MainView,
    GatherEnrollmentView, DonateView, MapView, MessagesContactView,
    DataLoaderView
)
from .flatpages import views

urlpatterns = [
    # basic app views
    url(r'^$', MainView.as_view(), name='home'),
    url(r'^how-to-gather$', GatherEnrollmentView.as_view(),
        name='how-to-gather'),
    url(r'^contact$', MessagesContactView.as_view(), name='envelope-contact'),
    url(r'^about$', AboutView.as_view(), name='about'),
    url(r'^help$', HelpView.as_view(), name='help'),
    url(r'^map$', MapView.as_view(), name='map'),
    url(r'^attributions$', AttributionsView.as_view(), name='attribution'),
    url(r'^donate$', DonateView.as_view(), name='donate'),
    url(r'^campaign/(?P<url>.*/)$', views.flatpage),
    url(
        r'^upload-form$', DataLoaderView.as_view(), name='upload-form'
    ),
]
