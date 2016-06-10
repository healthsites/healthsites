__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '10/06/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def json_serializer(locality):
    """
    serialize locality with clean json format
    """
    dict = locality.repr_dict(clean=True)
    for key in dict['values'].keys():
        dict[key] = dict['values'][key]
    dict.pop("values", None)
    return dict


def geojson_serializer(locality):
    """
    serialize locality with clean json format
    """
    dict = locality.repr_dict(clean=True)
    for key in dict['values'].keys():
        dict[key] = dict['values'][key]
    dict.pop("values", None)
    geojson = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": dict['geom']
        }
    }
    dict.pop("geom", None)
    geojson["properties"] = dict
    return geojson
