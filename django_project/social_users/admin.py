# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    Profile,
    TrustedUser,
    Organization
)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'profile_picture', 'screen_name')


admin.site.register(Profile, ProfileAdmin)


class OrganizationInline(admin.TabularInline):
    model = TrustedUser.organizations.through
    extra = 0  # how many rows to show


class TrustedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'list_organizations')
    inlines = (OrganizationInline,)

    def list_organizations(self, obj):
        return ", ".join(['<span><a href="/admin/social_users/organization/%s">%s</a></span>' % (p.id, p.name) for p in
                          obj.organizations.all()])

    list_organizations.allow_tags = True


admin.site.register(TrustedUser, TrustedUserAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'contact', 'list_trusted_user')

    def list_trusted_user(self, obj):
        return ", ".join(['<span><a href="/admin/social_users/trusteduser/%s">%s</a></span>' % (p.user.id, p.user.username) for p in
                          obj.trusted_users.all()])

    list_trusted_user.allow_tags = True


admin.site.register(Organization, OrganizationAdmin)
