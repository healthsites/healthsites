# coding=utf-8

__author__ = 'Muhammad Yarjuna Rohmat <myarjunar@kartoza.com>'
__date__ = '03/07/19'

import json
import requests
import random
import string
import zlib

from django.conf import settings
from django.http.response import HttpResponseBadRequest
from api.api_views.v2.base_api import BaseAPIWithAuth
from rest_framework.views import Response
from social_users.models import Organisation, OrganisationSupported, TrustedUser, GatherUser

GATHER_USERNAME = ''
GATHER_PASSWORD = ''
try:
    GATHER_USERNAME = settings.GATHER_USERNAME
    GATHER_PASSWORD = settings.GATHER_PASSWORD
except AttributeError:
    pass


class GatherEnrollment(BaseAPIWithAuth):
    """API to get the Gather ODK server settings."""

    def get_gather(self, server_url):
        """ GET gather """
        session = requests.Session()
        session.auth = (GATHER_USERNAME, GATHER_PASSWORD)
        r = session.get(server_url)
        return r

    def post_gather(self, server_url, payload):
        """ For post gather """
        # POST with form-encoded data
        session = requests.Session()
        session.auth = (GATHER_USERNAME, GATHER_PASSWORD)

        r = session.head(server_url)
        csrf_token = r.cookies.get('csrftoken')

        headers = {'X-csrftoken': csrf_token}
        r = session.post(server_url, json=payload, headers=headers)
        return r

    def put_gather(self, server_url, payload):
        """ For post gather """
        # POST with form-encoded data
        session = requests.Session()
        session.auth = (GATHER_USERNAME, GATHER_PASSWORD)

        r = session.head(server_url)
        csrf_token = r.cookies.get('csrftoken')

        headers = {'X-csrftoken': csrf_token}
        r = session.put(server_url, json=payload, headers=headers)
        return r

    def get(self, request):
        password_characters = string.ascii_letters + \
                              string.digits + string.punctuation
        # generate payload
        password = ''.join(random.choice(password_characters) for i in range(10))
        payload = {
            'username': request.user.username,
            'password': password}

        # GENERATE SURVEYOR
        response = self.post_gather(settings.GATHER_API_URL + 'odk/surveyors/', payload)
        if response.status_code == 201 or response.status_code == 200:
            pass
        elif response.status_code == 400:
            # ALREADY EXIST
            # CHANGE THE PASSWORD
            # SEARCH USER ID
            server_url = (settings.GATHER_API_URL +
                          'odk/surveyors/?search=%s' % request.user.username)
            response = self.get_gather(server_url)
            content = json.loads(response.content)
            if response.status_code == 201 or response.status_code == 200:
                for result in content['results']:
                    if result['username'] == request.user.username:
                        # IF USERNAME FOUND RESET PASSWORD
                        response = self.put_gather(
                            settings.GATHER_API_URL + 'odk/surveyors/%s/' % result['id'], payload)
                        if response.status_code == 201 or response.status_code == 200:
                            pass
                        else:
                            return HttpResponseBadRequest(response.text)
                        break

            else:
                return HttpResponseBadRequest(response.text)

        else:
            return HttpResponseBadRequest(response.text)

        data = {
            'general': {
                'server_url': settings.GATHER_API_URL_ODK,
                'username': request.user.username,
                'password': password,
            },
            'admin': {}}

        # create as trusted user
        try:
            organisation = Organisation.objects.get(name='gather')
            trusted_user, created = TrustedUser.objects.get_or_create(user=request.user)
            OrganisationSupported.objects.get_or_create(
                organisation=organisation, user=trusted_user)
        except Organisation.DoesNotExist:
            return HttpResponseBadRequest('Gather organisation not found')
        # create gather information
        compressed_data = zlib.compress(json.dumps(data), -1)
        return Response(compressed_data.encode('base64'))


class GatherTrustedUser(BaseAPIWithAuth):
    """API to add gather trusted user."""

    def post(self, request):
        try:
            organisation = Organisation.objects.get(name='gather')
            OrganisationSupported.objects.get_or_create(
                organisation=organisation, user=request.user)
        except Organisation.DoesNotExist:
            return HttpResponseBadRequest('Gather organisation not found')
