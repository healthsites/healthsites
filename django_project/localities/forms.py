# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import django.forms as forms


class DomainForm(forms.Form):
    lon = forms.FloatField()
    lat = forms.FloatField()

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain')

        super(DomainForm, self).__init__(*args, **kwargs)

        for spec in domain.specification_set.select_related('attribute'):
            field = forms.CharField(label=spec.attribute.key)
            self.fields[spec.attribute.key] = field


class LocalityForm(forms.Form):
    lon = forms.FloatField()
    lat = forms.FloatField()

    def __init__(self, *args, **kwargs):
        locality = kwargs.pop('locality')

        tmp_initial_data = {
            'lon': locality.geom.x, 'lat': locality.geom.y
        }

        # Locality forms are special as they automatcally collect initial data
        # based on the actual models
        for value in locality.value_set.select_related('attribute').all():
            tmp_initial_data.update({value.attribute.key: value.data})

        kwargs.update({'initial': tmp_initial_data})

        super(LocalityForm, self).__init__(*args, **kwargs)

        for spec in (
                locality.domain.specification_set.select_related('attribute')):
            field = forms.CharField(label=spec.attribute.key)
            self.fields[spec.attribute.key] = field
