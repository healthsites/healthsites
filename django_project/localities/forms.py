# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import django.forms as forms


class LocalityForm(forms.Form):
    lon = forms.FloatField()
    lat = forms.FloatField()

    def __init__(self, locality, *args, **kwargs):

        tmp_initial_data = {
            'lon': locality.geom.x, 'lat': locality.geom.y
        }

        for attr in locality.group.attribute_set.all():
            field = forms.CharField(label=attr.key)
            self.base_fields[attr.key] = field

        # Locality forms are special as they automatcally collect initial data
        # based on the actual models
        for value in locality.value_set.select_related('attribute').all():
            tmp_initial_data.update({value.attribute.key: value.data})

        kwargs.update({'initial': tmp_initial_data})

        super(LocalityForm, self).__init__(*args, **kwargs)
