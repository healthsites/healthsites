# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '09/04/19'

from pandas import DataFrame
from rest_framework.views import APIView
from rest_framework.response import Response
from sklearn.cluster import KMeans
from localities.utils import parse_bbox
from localities_osm.utilities import get_all_osm_query
from localities_osm.serializer.locality_osm_centroid import \
    LocalityOSMCentroidSerializer


class Clustering(APIView):
    """API to build cluster locality OSM using KMeans method."""

    def get(self, request):
        query = get_all_osm_query()

        bbox = request.GET.get('bbox', None)
        if bbox:
            bbox_geom = parse_bbox(bbox)
            query = query.in_bbox(bbox_geom)

        serializer = LocalityOSMCentroidSerializer(query, many=True)
        df = DataFrame(
            serializer.data,
            columns=['lat', 'lng'], index=None)

        response_data = []
        total = query.count()

        if total > 0:
            clusters = 20
            if total < 20:
                clusters = total

            kmeans = KMeans(n_clusters=clusters, max_iter=50).fit(df)
            samples = kmeans.predict(df)
            centroids = kmeans.cluster_centers_

            for i in range(len(centroids)):
                response_data.append({
                    'centroid_lat': centroids[i][0],
                    'centroid_lng': centroids[i][1],
                    'count': 0
                })

            for sample in samples:
                response_data[sample]['count'] += 1

            response = {
                'data': response_data,
                'cluster': 'true',
                'total_data': query.count(),
            }

        else:
            response = {
                'data': response_data,
                'cluster': 'false',
                'total_data': query.count()
            }

        return Response(response)
