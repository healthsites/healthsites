# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import (
    Domain,
    Attribute,
    Specification
)


class DomainMA(admin.ModelAdmin):
    fields = ('name', 'description', 'template_fragment')

admin.site.register(Domain, DomainMA)


class AttributeMA(admin.ModelAdmin):
    fields = ('key', 'description')

admin.site.register(Attribute, AttributeMA)


class SpecificationMA(admin.ModelAdmin):
    fields = ('domain', 'attribute', 'required')

admin.site.register(Specification, SpecificationMA)
