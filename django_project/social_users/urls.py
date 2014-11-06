# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import UserSigninPage, UserProfilePage, LogoutUser

urlpatterns = patterns(
    '',
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^signin$', UserSigninPage.as_view(), name='usersignpage'),
    url(r'^profile$', UserProfilePage.as_view(), name='userprofilepage'),
    url(r'^logout$', LogoutUser.as_view(), name='logout_user'),
)
