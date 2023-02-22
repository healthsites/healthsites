__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'

from django.conf import settings
from api.utilities.geometry import (
    within_bbox, update_minbbox, overlapping_area
)


def oms_view_cluster(localites, zoom, pix_x, pix_y):
    """
    Walk though a set of osm view and create point clusters

    We use a simple method that for every point, that is not within any
    cluster, calculate it's 'catchment' area and add it to the cluster

    If a point is within a cluster 'catchment' area increase point count for
    that cluster and recalculate clusters minimum bbox
    """

    cluster_points = []
    for locality in localites.iterator():
        try:
            geomx = locality.geometry.centroid.x
            geomy = locality.geometry.centroid.y
        except IndexError:
            continue

        # check every point in cluster_points
        for pt in cluster_points:
            if zoom != settings.MAX_ZOOM and within_bbox(pt['bbox'], geomx, geomy):
                # it's in the cluster 'catchment' area
                pt['count'] += 1
                pt['minbbox'] = update_minbbox((geomx, geomy), pt['minbbox'])
                break
        else:
            # point is not in the catchment area of any cluster
            x_range, y_range = overlapping_area(zoom, pix_x, pix_y, geomy)
            bbox = (
                geomx - x_range * 1.5, geomy - y_range * 1.5,
                geomx + x_range * 1.5, geomy + y_range * 1.5
            )
            new_cluster = {
                'uuid': '%s/%s' % (locality.osm_type, locality.osm_id),
                'geom': (geomx, geomy),
                'count': 1,
                'bbox': bbox,
                'minbbox': (geomx, geomy, geomx, geomy),
            }
            cluster_points.append(new_cluster)

    for cluster_point in cluster_points:
        try:
            del cluster_point['bbox']
        except KeyError:
            pass
    return cluster_points
