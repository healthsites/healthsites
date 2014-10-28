# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.views.generic import TemplateView


class MainView(TemplateView):
    template_name = 'main.html'
