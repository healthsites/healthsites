# -*- coding: utf-8 -*-

from django import forms
from django.forms import models
from localities.models import DataLoader


class DataLoaderForm(models.ModelForm):
    """Form for DataLoader.
    """

    class Meta:
        model = DataLoader
        fields = (
            'csv_data',
        )

    csv_data = forms.FileField(
        widget=forms.FileInput(
            attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(DataLoaderForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save method.
        """
        data_loader = super(DataLoaderForm, self).save(commit=False)
        data_loader.author = self.user
        data_loader.applied = False
        if commit:
            data_loader.save()
        return data_loader
