# -*- coding: utf-8 -*-
import logging

LOG = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.contrib.auth import logout as auth_logout
from braces.views import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from social_users.models import Profile
from localities.models import LocalityArchive, ValueArchive
from core.utilities import extract_time
# from localities.api import extract_updates
from django.db.models import Count, Max
from datetime import datetime
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder


class UserProfilePage(LoginRequiredMixin, TemplateView):
    template_name = 'social_users/profilepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(UserProfilePage, self).get_context_data(*args, **kwargs)
        context['auths'] = [
            auth.provider for auth in self.request.user.social_auth.all()
            ]
        return context


def getProfile(user):
    shared_links = []
    # check if the user has profile_picture
    # if not, just send empty string
    username = user.username
    try:
        user_detail = Profile.objects.get(user=user)
        profile_picture = user_detail.profile_picture
        if user_detail.screen_name != "":
            username = user_detail.screen_name
    except Profile.DoesNotExist:
        profile_picture = ""

    user.profile_picture = profile_picture
    user.screen_name = username
    user.shared_links = shared_links
    return user


class ProfilePage(TemplateView):
    template_name = 'social_users/profile.html'

    def get_context_data(self, *args, **kwargs):
        """
        *debug* toggles GoogleAnalytics support on the main page
        """

        user = get_object_or_404(User, username=kwargs["username"])
        user = getProfile(user)
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        context['user'] = user
        return context


class UserSigninPage(TemplateView):
    template_name = 'social_users/signinpage.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')


def get_username(strategy, details, user=None, *args, **kwargs):
    return {'name': details['username']}


def save_profile(backend, user, response, *args, **kwargs):
    url = None
    if backend.name == 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
    if backend.name == 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if backend.name == 'google-oauth2':
        url = response['image'].get('url')
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)

    # if there is an username
    if kwargs['name']:
        username = kwargs['name']

    profile.screen_name = username
    if url:
        profile.profile_picture = url
    profile.save()


def user_updates(user, date):
    updates = []
    try:
        updates1 = LocalityArchive.objects.filter(changeset__social_user=user).filter(
                changeset__created__lt=date).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username', 'version').annotate(
                edit_count=Count('changeset'), locality_id=Max('object_id'))[:15]
        for update in updates1:
            updates.append(update)
        updates2 = ValueArchive.objects.filter(changeset__social_user=user).filter(
                changeset__created__lt=date).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username', 'version').annotate(
                edit_count=Count('changeset'), locality_id=Max('locality_id'))[:15]
        for update in updates2:
            updates.append(update)
        updates.sort(key=extract_time, reverse=True)
    except LocalityArchive.DoesNotExist:
        print "Locality Archive not exist"

    output = []
    prev_changeset = 0
    for update in updates:
        if prev_changeset != update['changeset']:
            output.append(update)
            profile = getProfile(User.objects.get(username=update['changeset__social_user__username']))
            update['nickname'] = profile.screen_name
        prev_changeset = update['changeset']
    return output[:20]


def get_user_updates(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        user = request.GET.get('user')
        if not date:
            date = datetime.now()
        user = get_object_or_404(User, username=user)
        last_updates = user_updates(user, date)
        # updates = extract_updates(last_updates)
        result = {}
        # result['last_update'] = updates
        result = json.dumps(result, cls=DjangoJSONEncoder)

    return HttpResponse(result, content_type='application/json')
