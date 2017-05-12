# -*- coding: utf-8 -*-
import datetime

import factory
from social.apps.django_app.default.models import UserSocialAuth

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType


class ContentTypeF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "content type %s" % n)

    class Meta:
        model = ContentType


class PermissionF(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "permission%s" % n)
    content_type = factory.SubFactory(ContentTypeF)
    codename = factory.Sequence(lambda n: "factory_%s" % n)

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

    name = factory.Sequence(lambda n: "group%s" % n)

    class Meta:
        model = Group


class UserF(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: "username%s" % n)
    first_name = factory.Sequence(lambda n: "first_name%s" % n)
    last_name = factory.Sequence(lambda n: "last_name%s" % n)
    email = factory.Sequence(lambda n: "email%s@example.com" % n)
    password = factory.Sequence(lambda n: "password%s" % n)
    is_staff = False
    is_active = True
    is_superuser = False
    last_login = datetime.datetime(2000, 1, 1)
    date_joined = datetime.datetime(1999, 1, 1)

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserF, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user

    class Meta:
        model = User


class UserSocialAuthF(factory.django.DjangoModelFactory):
    user = factory.SubFactory('social_users.tests.model_factories.UserF')
    provider = factory.Sequence(lambda n: "provider%s" % n)
    uid = factory.Sequence(lambda n: "uid%s" % n)
    extra_data = {}

    class Meta:
        model = UserSocialAuth
