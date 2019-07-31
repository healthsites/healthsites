# coding=utf-8
from django import forms
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.gis import admin
from django.utils.safestring import mark_safe
from ckeditor.widgets import CKEditorWidget
from .models import CampaignPage
from api.models.user_api_key import UserApiKey


class CampaignPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = CampaignPage
        fields = '__all__'


class CampaignPageAdmin(FlatPageAdmin):
    form = CampaignPageAdminForm
    list_display = ('campaign_title', 'gather_url', 'organisation', 'campaign_page')

    fieldsets = (
        (None, {
            'fields':
                ('campaign_title',
                 'content',
                 'gather_url',
                 'organisation',
                 'api_key')}),
    )
    readonly_fields = ('api_key',)

    def campaign_page(self, obj):
        return mark_safe("""<a href="/campaign%s">%s</a>""" % (obj.url, obj.url))

    def api_key(self, obj):
        if obj.organisation and obj.organisation.organizer:
            try:
                api_key = UserApiKey.objects.get(
                    user=obj.organisation.organizer, is_active=True)
                return api_key.api_key
            except UserApiKey.DoesNotExist:
                pass
        return 'please assign organizer into organisation ' \
               'and create api key for the organizer'

    api_key.allow_tags = True
    api_key.short_description = \
        'Api key for this campaign. Use this on the gather authentication.'


admin.site.unregister(FlatPage)
admin.site.register(CampaignPage, CampaignPageAdmin)
