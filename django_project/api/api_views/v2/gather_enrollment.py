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

    def get(self, request):
        try:
            gather_user = GatherUser.objects.get(user=request.user)
            password = gather_user.gather_password
        except GatherUser.DoesNotExist:
            password_characters = string.ascii_letters + string.digits + string.punctuation
            # generate payload
            password = ''.join(random.choice(password_characters) for i in range(10))
            server_url = settings.GATHER_API_URL + 'odk/surveyors/'

            payload = {
                'username': request.user.username,
                'password': password}

            # POST with form-encoded data
            session = requests.Session()
            session.auth = (GATHER_USERNAME, GATHER_PASSWORD)

            r = session.head(server_url)
            csrf_token = r.cookies.get('csrftoken')

            headers = {'X-csrftoken': csrf_token}
            r = session.post(server_url, json=payload, headers=headers)
            if r.status_code == 201 or r.status_code == 200:
                content = json.loads(r.content)
                try:
                    gather_user = GatherUser(user=request.user)
                except GatherUser.DoesNotExist:
                    gather_user = GatherUser()
                gather_user.user = request.user
                gather_user.gather_id = content['id']
                gather_user.gather_password = password
                gather_user.save()

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
