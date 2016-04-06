# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    Profile,
    TrustedUser,
    Organisation
)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'profile_picture', 'screen_name')


admin.site.register(Profile, ProfileAdmin)


class OrganisationInline(admin.TabularInline):
    model = TrustedUser.organisations_supported.through
    extra = 0  # how many rows to show


class TrustedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'list_organisation_supported')
    inlines = (OrganisationInline,)

    def list_organisation_supported(self, obj):
        return ", ".join(['<span><a href="/admin/social_users/organisation/%s">%s</a></span>' % (p.id, p.name) for p in
                          obj.organisations_supported.all()])

    list_organisation_supported.allow_tags = True


admin.site.register(TrustedUser, TrustedUserAdmin)


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'contact', 'list_trusted_user')

    def list_trusted_user(self, obj):
        return ", ".join(['<span><a href="/admin/social_users/trusteduser/%s">%s</a></span>' % (p.user.id, p.user.username) for p in
                          obj.trusted_users.all()])

    list_trusted_user.allow_tags = True


admin.site.register(Organisation, OrganisationAdmin)
