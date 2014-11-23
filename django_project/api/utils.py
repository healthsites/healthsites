# -*- coding: utf-8 -*-


def remap_dict(old_dict, transform):
    """
    Rename specific dictionary keys
    """
    new_dict = {}
    for k, v in old_dict.items():
        if k in transform:
            new_dict.update({transform[k]: v})
        else:
            new_dict.update({k: v})
    return new_dict
