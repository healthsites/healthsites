# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    UserDetail, UserLink
)


class UserDetailAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'profile_picture')


admin.site.register(UserDetail, UserDetailAdmin)


class UserLinkAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'link')


admin.site.register(UserLink, UserLinkAdmin)
