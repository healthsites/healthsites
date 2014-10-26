# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.views.generic import TemplateView

from djgeojson.views import GeoJSONLayerView

from localities.models import Locality


class MainView(TemplateView):
    template_name = 'main.html'


class LocalitiesLayer(GeoJSONLayerView):
    # precision = 4   # float
    model = Locality
    properties = ['id']
