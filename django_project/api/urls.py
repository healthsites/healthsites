# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from api.api_views.v1 import ApiVersion1, ApiVersion2

urlpatterns = [
    url(r'v3/', include('api.urls_v3')),
    url(r'v2/', ApiVersion2.as_view()),
    url(r'v1/', ApiVersion1.as_view()),
    url(r'^', include('api.urls_schema')),
]
