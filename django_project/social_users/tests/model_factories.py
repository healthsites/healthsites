# -*- coding: utf-8 -*-
import datetime

import factory
from social.apps.django_app.default.models import UserSocialAuth

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.utils.timezone import now

from ..models import Organisation, OrganisationSupported, Profile, TrustedUser


class ContentTypeF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'content type %s' % n)

    class Meta:
        model = ContentType


class PermissionF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'permission%s' % n)
    content_type = factory.SubFactory(ContentTypeF)
    codename = factory.Sequence(lambda n: 'factory_%s' % n)

    class Meta:
        model = Permission


class GroupF(factory.django.DjangoModelFactory):
    @classmethod
    def _setup_next_sequence(cls):
        try:
            return cls._associated_class.objects.values_list(
                'id', flat=True).order_by('-id')[0] + 1
        except IndexError:
            return 0

    name = factory.Sequence(lambda n: 'group%s' % n)

    class Meta:
        model = Group


class UserF(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'username%s' % n)
    first_name = factory.Sequence(lambda n: 'first_name%s' % n)
    last_name = factory.Sequence(lambda n: 'last_name%s' % n)
    email = factory.Sequence(lambda n: 'email%s@example.com' % n)
    password = factory.PostGenerationMethodCall('set_password', 'password')
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = datetime.datetime(2000, 1, 1)
    date_joined = datetime.datetime(1999, 1, 1)

    class Meta:
        model = User


class SiteF(factory.django.DjangoModelFactory):
    domain = 'http://healthsites.io'
    name = 'Healthsites'

    class Meta:
        model = Site


class UserSocialAuthF(factory.django.DjangoModelFactory):
    user = factory.SubFactory('social_users.tests.model_factories.UserF')
    provider = factory.Sequence(lambda n: 'provider%s' % n)
    uid = factory.Sequence(lambda n: 'uid%s' % n)
    extra_data = {}

    class Meta:
        model = UserSocialAuth


class ProfileF(factory.django.DjangoModelFactory):
    user = factory.SubFactory('social_users.tests.model_factories.UserF')
    profile_picture = ''

    class Meta:
        model = Profile


class TrustedUserF(factory.django.DjangoModelFactory):
    user = factory.SubFactory('social_users.tests.model_factories.UserF')

    class Meta:
        model = TrustedUser


class OrganisationF(factory.django.DjangoModelFactory):
    name = ''
    site = factory.SubFactory('social_users.tests.model_factories.SiteF')
    contact = ''

    class Meta:
        model = Organisation


class OrganisationSupportedF(factory.django.DjangoModelFactory):
    organisation = factory.SubFactory('social_users.tests.model_factories.OrganisationF')
    user = factory.SubFactory('social_users.tests.model_factories.TrustedUserF')
    is_staff = False
    date_added = factory.LazyFunction(now)

    class Meta:
        model = OrganisationSupported


class UserWith2OrganisationSupportedF(TrustedUserF):
    orgsupported1 = factory.RelatedFactory(
        'social_users.tests.model_factories.OrganisationSupportedF', 'user'
    )
    orgsupported2 = factory.RelatedFactory(
        'social_users.tests.model_factories.OrganisationSupportedF', 'user'
    )
