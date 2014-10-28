# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import MainView

urlpatterns = patterns(
    '',
    # basic app views
    url(r'^$', MainView.as_view(), name='home')
)
