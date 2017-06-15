# -*- coding: utf-8 -*-
import logging

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, View

from braces.views import LoginRequiredMixin

from social_users.utils import get_profile

LOG = logging.getLogger(__name__)


class UserProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'social_users/profilepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfilePage, self).get_context_data(*args, **kwargs)
        context['auths'] = [
            auth.provider for auth in self.request.user.social_auth.all()
        ]
        return context


class ProfilePage(TemplateView):
    template_name = 'social_users/profile.html'

    def get_context_data(self, *args, **kwargs):
        """
        *debug* toggles GoogleAnalytics support on the main page
        """

        user = get_object_or_404(User, username=kwargs['username'])
        user = get_profile(user)
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        context['user'] = user
        return context


class UserSigninPage(TemplateView):
    template_name = 'social_users/signinpage.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')
