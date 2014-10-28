# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import LocalitiesLayer, LocalityInfo

urlpatterns = patterns(
    '',
    url(
        r'^localities.json$',
        LocalitiesLayer.as_view(), name='localities'
    ),
    url(
        r'^localities/(?P<pk>\d+)$', LocalityInfo.as_view(),
        name='locality-info')
)
