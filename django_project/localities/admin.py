# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Domain, Locality, Value, Attribute


class DomainMA(admin.ModelAdmin):
    pass

admin.site.register(Domain, DomainMA)


class LocalityMA(admin.ModelAdmin):
    pass

admin.site.register(Locality, LocalityMA)


class ValueMA(admin.ModelAdmin):
    pass

admin.site.register(Value, ValueMA)


class AttributeMA(admin.ModelAdmin):
    pass

admin.site.register(Attribute, AttributeMA)
