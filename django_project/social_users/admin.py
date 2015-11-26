# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    UserDetail
)


class UserDetailAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'profile_picture')


admin.site.register(UserDetail, UserDetailAdmin)
