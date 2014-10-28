# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import MainView, LocalitiesLayer, LocalityInfo

urlpatterns = patterns(
    '',
    # basic app views
    url(r'^$', MainView.as_view(), name='home'),
    url(
        r'^localities.json$',
        LocalitiesLayer.as_view(), name='localities'
    ),
    url(
        r'^localities/(?P<pk>\d+)$', LocalityInfo.as_view(),
        name='locality-info')
)
