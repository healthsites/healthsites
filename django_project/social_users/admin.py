# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    Profile
)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'profile_picture', 'screen_name')


admin.site.register(Profile, ProfileAdmin)
