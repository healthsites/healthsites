# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    Country,
    Domain,
    Attribute,
    Specification,
    Changeset,
    DataLoader,
    DataLoaderPermission,
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
    list_display = (
        'organisation_name', 'author', 'data_loader_mode', 'date_time_uploaded', 'applied', 'date_time_applied')


admin.site.register(DataLoader, DataUpdateAdmin)


class DataLoaderPermissionAdmin(admin.ModelAdmin):
    list_display = (
        'uploader', 'accepted_csv',)


admin.site.register(DataLoaderPermission, DataLoaderPermissionAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'polygon_geometry',)


admin.site.register(Country, CountryAdmin)
