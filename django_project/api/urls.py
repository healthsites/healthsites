# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import LocalitiesAPI, LocalityAPI

urlpatterns = patterns(
    '',
    url(
        r'^localities$', LocalitiesAPI.as_view(),
        name='api_localities'
    ),
    url(
        r'^locality/(?P<uuid>\w{32})$', LocalityAPI.as_view(),
        name='api_locality'
    )
)
