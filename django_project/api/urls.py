# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import LocalitiesAPI, LocalityAPI, LocalityDetail

urlpatterns = patterns(
    '',
    url(
        r'^localities$', LocalitiesAPI.as_view(),
        name='api_localities'
    ),
    url(
        r'^locality/(?P<uuid>\w{32})$', LocalityAPI.as_view(),
        name='api_locality'
    ),
    url(
        r'^v1/healthsites/facility/details',
        'api.views.LocalityDetail',
        name='api_locality_detail'
    )
)
