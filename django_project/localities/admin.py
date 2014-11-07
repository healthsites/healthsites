# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Domain,
    Attribute,
    Specification,
    Changeset
)


class ChangesetMixin():
    """
    Record a changeset and increase version number
    """
    def save_model(self, request, obj, form, change):
        if form.has_changed():
            chgset = Changeset.objects.create()
            obj.changeset = chgset
            obj.inc_version()
        obj.save()


class DomainMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('name', 'description', 'template_fragment')

admin.site.register(Domain, DomainMA)


class AttributeMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('key', 'description')

admin.site.register(Attribute, AttributeMA)


class SpecificationMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('domain', 'attribute', 'required')

admin.site.register(Specification, SpecificationMA)
