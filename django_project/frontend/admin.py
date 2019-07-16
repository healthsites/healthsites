# coding=utf-8
from django import forms
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.gis import admin
from ckeditor.widgets import CKEditorWidget
from .models import CustomFlatPage


class CustomFlatPageForm(forms.ModelForm):
    gather_url = forms.CharField(max_length=250)
    gather_username = forms.CharField(max_length=250)
    gather_password = forms.CharField(max_length=250)
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = CustomFlatPage
        fields = [
            'gather_url',
            'gather_username',
            'gather_password'
        ]


class CustomFlatPageAdmin(FlatPageAdmin):
    form = CustomFlatPageForm

    fieldsets = (
        (None, {'fields':
                ('enrollment_title',
                 'content',
                 'sites',
                 'gather_url',
                 'gather_username',
                 'gather_password')}),
    )


admin.site.unregister(FlatPage)
admin.site.register(CustomFlatPage, CustomFlatPageAdmin)
