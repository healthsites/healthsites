# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (
    LocalitiesLayer,
    LocalityInfo,
    LocalityUpdate,
    LocalityCreate
)

urlpatterns = patterns(
    '',
    url(
        r'^localities.json$', LocalitiesLayer.as_view(),
        name='localities'
    ),
    url(
        r'^localities/(?P<uuid>\w{32})$', LocalityInfo.as_view(),
        name='locality-info'
    ),
    url(
        r'^localities/(?P<uuid>\w{32})/form$', LocalityUpdate.as_view(),
        name='locality-update'
    ),
    url(
        r'^localities/form/(?P<domain>\w+)$', LocalityCreate.as_view(),
        name='locality-create'
    )
)
