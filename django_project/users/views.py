# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.contrib.auth import logout as auth_logout


class UserProfilePage(TemplateView):
    template_name = 'userprofilepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(
            UserProfilePage, self).get_context_data(*args, **kwargs)
        context['auths'] = [
            auth.provider for auth in self.request.user.social_auth.all()]
        return context


class UserSigninPage(TemplateView):
    template_name = 'usersigninpage.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')
