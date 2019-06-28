# -*- coding: utf-8 -*-
from social_django.admin import UserSocialAuth

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User

from social_users.models import Profile, TrustedUser

from .models import Organisation


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'profile_picture')


admin.site.register(Profile, ProfileAdmin)


class OrganisationInline(admin.TabularInline):
    model = TrustedUser.organisations_supported.through
    extra = 0  # how many rows to show


class TrustedUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'list_organisation_supported')
    inlines = (OrganisationInline,)

    def list_organisation_supported(self, obj):
        template_format = '<span><a href="/admin/social_users/organisation/%s">%s</a></span>'
        return ', '.join(
            [template_format % (p.id, p.name) for p in obj.organisations_supported.all()]
        )

    list_organisation_supported.allow_tags = True


admin.site.register(TrustedUser, TrustedUserAdmin)


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('name', 'site', 'contact', 'organizer', 'list_trusted_user')

    def list_trusted_user(self, obj):
        template_format = '<span><a href="/admin/social_users/trusteduser/%s">%s</a></span>'
        return ', '.join(
            [template_format % (p.user.id, p.user.username) for p in obj.trusted_users.all()]
        )

    list_trusted_user.allow_tags = True


admin.site.register(Organisation, OrganisationAdmin)


class UserProfileInline(admin.TabularInline):
    model = Profile
    fk_name = 'user'
    can_delete = True
    max_num = 1
    extra = 0


class SocialAuthInline(admin.TabularInline):
    model = UserSocialAuth
    fk_name = 'user'
    can_delete = True
    extra = 0


class TrustedUserInline(admin.TabularInline):
    model = TrustedUser
    readonly_fields = ('is_trusted', 'list_organisations')
    fk_name = 'user'
    can_delete = False
    max_num = 0
    extra = 0

    def is_trusted(self, obj):
        template_format = (
            '<a href="/admin/social_users/trusteduser/%s">'
            '<img src="/static/admin/img/icon-yes.gif" alt="True"></a>'
        )
        return template_format % obj.id

    def list_organisations(self, obj):
        template_format = '<span><a href="/admin/social_users/organization/%s">%s</a></span>'
        return ', '.join(
            [template_format % (p.id, p.name) for p in obj.organisations_supported.all()]
        )

    is_trusted.allow_tags = True
    list_organisations.allow_tags = True


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'email', 'is_staff', 'provider', 'profile_picture', 'is_trusted')
    inlines = (UserProfileInline, SocialAuthInline, TrustedUserInline)

    def provider(self, obj):
        try:
            template_format = '<span><a href="/admin/default/usersocialauth/%s">%s</a></span>'
            return ', '.join([
                template_format % (p.id, p.provider)
                for p in UserSocialAuth.objects.filter(user=obj)
            ])
        except UserSocialAuth.DoesNotExist:
            return ''

    def profile_picture(self, obj):
        try:
            return ', '.join([
                '<span><a href="%s">%s</a></span>' % (p.profile_picture, p.profile_picture)
                for p in Profile.objects.filter(user=obj)
            ])
        except UserSocialAuth.DoesNotExist:
            return ''

    def is_trusted(self, obj):
        try:
            detail = TrustedUser.objects.get(user=obj)
            template_format = (
                '<a href="/admin/social_users/trusteduser/%s">'
                '<img src="/static/admin/img/icon-yes.gif" alt="True"></a>'
            )
            return template_format % detail.id
        except TrustedUser.DoesNotExist:
            return '<img src="/static/admin/img/icon-no.gif" alt="False">'

    provider.allow_tags = True
    profile_picture.allow_tags = True
    is_trusted.allow_tags = True


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
