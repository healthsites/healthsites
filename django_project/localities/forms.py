# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import django.forms as forms
from django.forms import models

from .models import Domain, DataLoader
from .utils import render_fragment


class DomainModelForm(forms.ModelForm):
    """
    Used in django admin

    Special validation rules for template_fragment field
    """

    class Meta:
        model = Domain
        fields = ('name', 'description', 'template_fragment')

    def clean_template_fragment(self):
        try:
            render_fragment(self.cleaned_data['template_fragment'], {})
        except Exception, e:
            raise forms.ValidationError(
                'Template Syntax Error: {}'.format(e.message)
            )

        return self.cleaned_data['template_fragment']


class DomainForm(forms.Form):
    """
    Used when creating a new Locality

    Form will dynamically add every specification of an attribute as a simple
    CharField
    """

    lon = forms.FloatField()
    lat = forms.FloatField()

    def __init__(self, *args, **kwargs):
        # pop arguments which are not form fields
        domain = kwargs.pop('domain')

        super(DomainForm, self).__init__(*args, **kwargs)

        # populate form with attribute specifications
        for spec in domain.specification_set.select_related('attribute'):
            field = forms.CharField(
                label=spec.attribute.key, required=spec.required
            )
            self.fields[spec.attribute.key] = field


class LocalityForm(forms.Form):
    """
    Used when updating a Locality

    Form will dynamically add every specification of an attribute as a simple
    CharField, and prefill it with initial values
    """

    lon = forms.FloatField()
    lat = forms.FloatField()

    def __init__(self, *args, **kwargs):
        # pop arguments which are not form fields
        locality = kwargs.pop('locality')

        tmp_initial_data = {
            'lon': locality.geom.x, 'lat': locality.geom.y
        }

        # Locality forms are special as they automatically collect initial data
        # based on the actual models
        for value in locality.value_set.select_related('specification').all():
            tmp_initial_data.update({
                value.specification.attribute.key: value.data
            })

        # set initial form data
        kwargs.update({'initial': tmp_initial_data})

        super(LocalityForm, self).__init__(*args, **kwargs)

        for spec in (
                locality.domain.specification_set.select_related('attribute')):

            field = forms.CharField(
                label=spec.attribute.key, required=spec.required
            )
            self.fields[spec.attribute.key] = field
            self.fields[spec.attribute.key].widget.attrs.update(
                {'class': 'form-control'})


class DataLoaderForm(models.ModelForm):
    """Form for DataLoader.
    """
    class Meta:
        model = DataLoader
        fields = (
            'organisation_name',
            'json_concept_mapping',
            'csv_data',
            'data_loader_mode',
        )

    organisation_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )

    json_concept_mapping = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control'})
    )

    csv_data = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control'})
    )

    data_loader_mode = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={'class': 'form-control'}),
        choices=DataLoader.DATA_LOADER_MODE_CHOICES,
        initial=DataLoader.REPLACE_DATA_CODE,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DataLoaderForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save method.
        """
        data = self.cleaned_data
        data_loader = super(DataLoaderForm, self).save(commit=False)
        data_loader.author = self.user
        data_loader.applied = False
        if commit:
            data_loader.save()
        return data_loader

class SearchForm(forms.Form):
    """Form for search"""
    geoname = forms.CharField(
        label='Geoname'
    )
    locality_name = forms.CharField(
        label='Locality'
    )