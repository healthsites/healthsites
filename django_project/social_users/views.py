# -*- coding: utf-8 -*-
import os
import json
import logging
from datetime import datetime

from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, View

from braces.views import LoginRequiredMixin

from api.models.user_api_key import UserApiKey
from core.utilities import extract_time
from localities.models import Locality
from localities.utils import (
    extract_updates,
    get_update_detail,
)
from localities_osm.models.locality import LocalityOSMView
from localities_osm.serializer.locality_osm import LocalityOSMProfileSerializer
from social_users.models import Profile
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

        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        try:
            user = User.objects.get(username=kwargs['username'])
            user = get_profile(user, self.request)
            osm_user = False

            if self.request.user == user:
                # this is for checking availability old data
                old_data = Locality.objects.filter(
                    changeset__social_user__username=user, migrated=False
                )

                if old_data:
                    context['old_data_available'] = True

                pathname = \
                    os.path.join(
                        settings.CLUSTER_CACHE_DIR, 'data-migration-progress')
                progress_file = \
                    os.path.join(pathname, '{}.txt'.format(user))
                found = os.path.exists(progress_file)

                if found:
                    context['data_migration_in_progress'] = True

                autogenerate_api_key = False
                if user.is_superuser:
                    autogenerate_api_key = True
                context['api_keys'] = UserApiKey.get_user_api_key(
                    self.request.user, autogenerate=autogenerate_api_key)
        except User.DoesNotExist:
            user = {
                'username': kwargs['username']
            }
            osm_user = True

        context['user'] = user
        context['osm_user'] = osm_user
        context['api_keys'] = None
        return context


class UserSigninPage(TemplateView):
    template_name = 'social_users/signinpage.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')


def save_profile(backend, user, response, *args, **kwargs):
    # get old user
    if kwargs['is_new']:
        if 'username' in kwargs['details']:
            new_username = kwargs['details']['username']
            new_username = new_username.replace(' ', '')
            if user.username != new_username:
                try:
                    old_username = user.username
                    user = User.objects.get(username=new_username)
                    User.objects.get(username=old_username).delete()
                except User.DoesNotExist:
                    pass

    profile_picture = None
    if backend.name == 'facebook':
        profile_picture = 'http://graph.facebook.com/%s/picture?type=large' % response['id']
    elif backend.name == 'twitter':
        profile_picture = response.get('profile_image_url', '').replace('_normal', '')
    elif backend.name == 'google-oauth2':
        profile_picture = response['image'].get('url')
    elif backend.name == 'openstreetmap':
        profile_picture = response['avatar']

    Profile.objects.get_or_create(user=user)
    kwargs['request'].session['social_auth'] = {
        'profile_picture': profile_picture,
        'provider': backend.name
    }

    return {'user': user}


def user_updates(user, date):
    updates = []

    # get from locality osm for osm users
    updates_osm = \
        LocalityOSMView.objects.filter(
            changeset_user=user).order_by('-changeset_timestamp')
    serializer = LocalityOSMProfileSerializer(updates_osm, many=True)

    for update in serializer.data:
        updates.append(get_update_detail(update))

    updates.sort(key=extract_time, reverse=True)
    return updates[:10]


def get_user_updates(request):
    if request.method == 'GET':
        date = request.GET.get('date')
        user = request.GET.get('user')
        if not date:
            date = datetime.now()

        last_updates = user_updates(user, date)

        updates = extract_updates(last_updates)
        result = {}
        result['last_update'] = updates
        result = json.dumps(result, cls=DjangoJSONEncoder)

    return HttpResponse(result, content_type='application/json')
