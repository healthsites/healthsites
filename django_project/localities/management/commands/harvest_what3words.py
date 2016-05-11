__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/05/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'
# -*- coding: utf-8 -*-
import json
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from localities.models import Attribute, Domain, Changeset, Locality, Specification


class Command(BaseCommand):
    help = 'harvest what three word for localities'

    def handle(self, *args, **options):
        # get user that responsibility to change this
        user = None
        try:
            user = User.objects.get(username="sharehealthdata")
        except User.DoesNotExist:
            try:
                user = User.objects.get(username="admin")
            except User.DoesNotExist:
                pass
        # check attributes of what3word
        self.check_what3words_attribute(user)

        # create changeset
        changeset = Changeset.objects.create(social_user=user)

        # harvest what3words
        localities = Locality.objects.all()
        numbers = len(localities)
        index = 1
        for locality in localities:
            print "%d / %d" % (index, numbers)
            locality.update_what3words(user, changeset)
            index += 1

    def check_what3words_attribute(self, user):
        try:
            Attribute.objects.get(key='what3words')
        except Attribute.DoesNotExist:
            tmp_changeset = Changeset.objects.create(
                social_user=user
            )
            attribute = Attribute()
            attribute.key = 'what3words'
            attribute.changeset = tmp_changeset
            attribute.save()
            domain = Domain.objects.get(name="Health")
            specification = Specification()
            specification.domain = domain
            specification.attribute = attribute
            specification.changeset = tmp_changeset
            specification.save()
