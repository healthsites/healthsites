# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Domain,
    Attribute,
    Specification,
    Changeset,
    DataLoader
)

from .forms import DomainModelForm


class ChangesetMixin():
    """
    In order to create or update any model that uses models.ChangesetMixin we
    need to override Django admin *save_model* and create a new changeset
    """

    def save_model(self, request, obj, form, change):
        tmp_chgset = Changeset()
        tmp_chgset.social_user = request.user
        tmp_chgset.save()
        obj.changeset = tmp_chgset
        obj.save()


class DomainMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('name', 'description', 'template_fragment')
    form = DomainModelForm

admin.site.register(Domain, DomainMA)


class AttributeMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('key', 'description')

admin.site.register(Attribute, AttributeMA)


class SpecificationMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('domain', 'attribute', 'required')

admin.site.register(Specification, SpecificationMA)


class DataUpdateAdmin(admin.ModelAdmin):
    pass

admin.site.register(DataLoader, DataUpdateAdmin)
