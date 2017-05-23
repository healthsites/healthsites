# -*- coding: utf-8 -*-
import logging
import math

LOG = logging.getLogger(__name__)


def within_bbox(bbox, geomx, geomy):
    """
    Check if a point (geomx, geomy) is within a bbox (minx, miny, maxx, maxy)
    """

    if bbox[0] < geomx < bbox[2] and bbox[1] < geomy < bbox[3]:
        return True
    else:
        return False


def overlapping_area(zoom, pix_x, pix_y, lat):
    """
    Calculate an area (lng_deg, lat_deg) in degrees for an icon and a zoom

    Since we are using a World Mercator projection deformation is uniform in
    all directions and depends only on latitude
    """
    C = (2 * 6378137.0 * math.pi) / 256.  # one pixel
    C2 = (2 * 6378137.0 * math.pi) / 360.  # one degree

    lat_deformation = (C * math.cos(math.radians(lat)) / 2 ** zoom)

    lat_deg = (lat_deformation * pix_y) / C2
    lng_deg = (lat_deformation * pix_x) / C2

    return (lng_deg, lat_deg)


def update_minbbox(point, minbbox):
    """
    For every cluster we are calculating minimum bbox for Localities in the
    cluster

    This is required in order to have nicer click to zoom map behaviour
    (fitBounds)
    """

    new_minbbox = list(minbbox)

    if point[0] < minbbox[0]:
        new_minbbox[0] = point[0]
    if point[0] > minbbox[2]:
        new_minbbox[2] = point[0]
    if point[1] < minbbox[1]:
        new_minbbox[1] = point[1]
    if point[1] > minbbox[3]:
        new_minbbox[3] = point[1]

    return new_minbbox


def cluster(query_set, zoom, pix_x, pix_y, localities_is_needed=False):
    """
    Walk though a set of Localities and create point clusters

    We use a simple method that for every point, that is not within any
    cluster, calculate it's 'catchment' area and add it to the cluster

    If a point is within a cluster 'catchment' area increase point count for
    that cluster and recalculate clusters minimum bbox
    """

    cluster_points = []

    localites = query_set.get_lnglat().values(
        'id', 'name', 'uuid', 'lnglat', 'changeset__created'
    )
    number = localites.count()
    index = 1
    for locality in localites.iterator():
        if localities_is_needed:
            print '%s/%s' % (index, number)
        index += 1
        geomx, geomy = map(float, locality['lnglat'].split(','))

        # check every point in cluster_points
        for pt in cluster_points:
            if within_bbox(pt['bbox'], geomx, geomy):
                # it's in the cluster 'catchment' area
                pt['count'] += 1
                pt['minbbox'] = update_minbbox((geomx, geomy), pt['minbbox'])
                if localities_is_needed:
                    pt['localities'].append(locality)
                break

        else:
            # point is not in the catchment area of any cluster
            x_range, y_range = overlapping_area(zoom, pix_x, pix_y, geomy)
            locality_name = locality['name']
            bbox = (
                geomx - x_range * 1.5, geomy - y_range * 1.5,
                geomx + x_range * 1.5, geomy + y_range * 1.5
            )
            new_cluster = {
                'uuid': locality['uuid'],
                'name': locality_name,
                'count': 1,
                'geom': (geomx, geomy),
                'bbox': bbox,
                'minbbox': (geomx, geomy, geomx, geomy),
                'localities': []
            }
            if localities_is_needed:
                new_cluster['localities'].append(locality)

            cluster_points.append(new_cluster)

    return cluster_points
