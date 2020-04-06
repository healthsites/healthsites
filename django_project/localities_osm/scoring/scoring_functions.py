# coding=utf-8
import json


class AttributeScore:

    attributes = [
        'class_name',
    ]

    def __init__(self, value):
        if isinstance(value, basestring) or isinstance(value, str):
            self.json_string = value
            self.parse(value)
        else:
            self.dictionary = value
            self.parse_from_dict(value)

    def parse(self, json_string):
        obj = json.loads(json_string)
        self.parse_from_dict(obj)

    def parse_from_dict(self, dictionary):
        for key in self.attributes:
            setattr(self, key, dictionary[key])

    def function(self, *args, **kwargs):
        raise NotImplementedError


class KeyExistsScore(AttributeScore):

    attributes = [
        'attribute_name',
        'attribute_score_map',
        'ignore_case'
    ] + AttributeScore.attributes

    def key_score_map_value(self, key):
        ignore_case = bool(getattr(self, 'ignore_case', True))
        for map_key, map_value in self.attribute_score_map.items():
            if ignore_case:
                if key.lower() == map_key.lower():
                    return map_value
        return 0

    def function(self, value):
        return self.key_score_map_value(getattr(value, self.attribute_name))


class WeightedIndicatorScore(AttributeScore):

    attributes = [
        'weight',
        'score_function',
    ]

    def function(self, value):
        score_function_class_name = self.score_function['class_name']
        score_function_instance = generator_registry[
            score_function_class_name](self.score_function)
        return self.weight * score_function_instance.function(value)


class SumAttributeScore(AttributeScore):
    """Composite of list of Attribute Score"""

    attributes = [
        # list of score functions
        'score_functions',
    ] + AttributeScore.attributes

    def function(self, value):
        sum = 0
        for f in self.score_functions:
            class_name = f['class_name']
            Clazz = generator_registry[class_name]
            score_instance = Clazz(f)
            score = score_instance.function(value)
            sum += score
        return sum


generator_registry = {
    'KeyExistsScore': KeyExistsScore,
    'SumAttributeScore': SumAttributeScore
}
