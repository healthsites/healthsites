# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from braces.views import JSONResponseMixin

from localities.models import Locality

from .utils import remap_dict


class LocalitiesAPI(JSONResponseMixin, View):
    model = Locality

    def get(self, request, *args, **kwargs):

        # iterate thorugh queryset and remap keys
        transform = {
            'changeset__social_user_id': 'user_id'
        }
        object_list = [
            remap_dict(loc, transform)
            for loc in Locality.objects.select_related('changeset')
            .extra(select={'lnglat': 'st_x(geom)||$$,$$||st_y(geom)'})
            .values(
                'uuid', 'lnglat', 'version', 'changeset__social_user_id',
                # 'changeset__created'
            )
        ]

        return self.render_json_response(object_list)


class LocalityAPI(JSONResponseMixin, SingleObjectMixin, View):
    model = Locality
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_json_response(self.object.repr_dict())
