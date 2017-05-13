# -*- coding: utf-8 -*-

from api.serializer.locality_serializer import geojson_serializer, json_serializer
from api.views.api_view import ApiView
from localities.models import Locality, SynonymLocalities


class LocalitySynonymApiView(ApiView):
    """ Retrieve synonym of a facility"""

    def synonyms_to_json(self, synonyms, format):
        """ Format synonym to json
        :param query: query that will be formatted
        :type query: Queryset

        :param format: format type
        :type format: str

        :return: json based on format
        :rtype: dict
        """
        output = []
        for synonym in synonyms:
            if format == 'geojson':
                output.append(geojson_serializer(synonym.synonym))
            else:
                output.append(json_serializer(synonym.synonym))
        return output

    def get(self, request, *args, **kwargs):
        validation = self.extract_request(request)
        if validation:
            return self.api_response(
                {'error': validation}
            )

        # check uuid for this
        if 'uuid' not in request.GET:
            return self.api_response(
                {'error': "parameter is not enough"}
            )

        uuid = request.GET['uuid']
        try:
            locality = Locality.objects.get(uuid=uuid)
        except Locality.DoesNotExist:
            return self.api_response(
                {'error': "facility isn't found"}
            )

        synonyms = SynonymLocalities.objects.filter(locality=locality)
        facilities = self.synonyms_to_json(synonyms, self.format)
        return self.api_response(facilities)
