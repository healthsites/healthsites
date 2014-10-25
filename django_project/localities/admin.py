# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Group, Locality, Value, Attribute


class GroupMA(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupMA)


class LocalityMA(admin.ModelAdmin):
    pass

admin.site.register(Locality, LocalityMA)


class ValueMA(admin.ModelAdmin):
    pass

admin.site.register(Value, ValueMA)


class AttributeMA(admin.ModelAdmin):
    pass

admin.site.register(Attribute, AttributeMA)
