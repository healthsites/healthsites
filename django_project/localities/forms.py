# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import django.forms as forms


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

        for attr in locality.domain.attribute_set.all():
            field = forms.CharField(label=attr.key)
            self.fields[attr.key] = field
