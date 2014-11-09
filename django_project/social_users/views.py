# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.contrib.auth import logout as auth_logout
from braces.views import LoginRequiredMixin


class UserProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'social_users/profilepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            UserProfilePage, self).get_context_data(*args, **kwargs)
        context['auths'] = [
            auth.provider for auth in self.request.user.social_auth.all()
        ]
        return context


class UserSigninPage(TemplateView):
    template_name = 'social_users/signinpage.html'


class LogoutUser(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')
