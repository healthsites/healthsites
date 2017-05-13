# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from localities.models import Attribute, Changeset, Domain, Locality, Specification, Value


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
            try:
                value = Value.objects.get(
                    specification__attribute__key='what3words',
                    locality=locality)
                print value.locality, value.data
            except Value.DoesNotExist:
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
