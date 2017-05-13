# -*- coding: utf-8 -*-


def json_serializer(locality):
    """ Serialize locality with clean json format
    """
    dict = locality.repr_dict(clean=True)

    for key in dict['values'].keys():
        dict[key] = dict['values'][key]
    dict.pop('values', None)
    return dict


def geojson_serializer(locality):
    """ Serialize locality with clean geojson format
    """

    dict = locality.repr_dict(clean=True)

    for key in dict['values'].keys():
        dict[key] = dict['values'][key]
    dict.pop('values', None)

    geojson = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': dict['geom']
        }
    }
    dict.pop('geom', None)
    geojson['properties'] = dict
    return geojson
