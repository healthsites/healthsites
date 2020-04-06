__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models
from localities_osm.scoring.scoring_functions import \
    generator_registry


class LocalityOSMBase(models.Model):
    _DATABASE = 'docker_osm'

    class Meta:
        abstract = True


class LocalityOSMScoreMixin:
    """Mixin class to provide row based scoring of entry."""

    def calculate_score(self):
        raise NotImplementedError

    def reset_score(self):
        raise NotImplementedError

    def is_score_calculated(self):
        raise NotImplementedError


class COVID19LocalityOSMScore(LocalityOSMScoreMixin):
    """This class contains basic rules to update rows of
    caches of attributes scores.

    Rules are hardcoded now, but is expected to be taken from a json
    serializable configurations that is stored in the database.
    These rules might be configured by users from the admin page.
    A rule might be associated with a django form field as widget.
    """

    # django model field for score caches
    score_health_facility_type = models.DecimalField(
        null=True,
        default=0)
    # Should add more score caches from different attributes here
    # This one is the total score
    total_score_covid19 = models.DecimalField(
        null=True,
        default=0)

    # Denotes wether the score caches are already calculated
    score_covid19_calculated = models.BooleanField(
        null=False,
        default=False)

    _score_health_facility_definitions = {
        'class_name': 'WeightedIndicatorScore',
        'weight': 2,
        'score_function': {
            'class_name': 'KeyExistsScore',
            'attribute_name': 'amenity',
            'attribute_score_map': {
                'hospital': 2,
                'clinic': 1
            }
        }
    }

    _total_scoring_definitions = {
        'class_name': 'SumAttributeScore',
        'score_functions': [
            _score_health_facility_definitions,
        ]
    }

    def calculate_score(self):
        # TODO: Should handle queryset instead of individual rows
        class_name = self._score_health_facility_definitions['class_name']
        scoring_function_instance = generator_registry[class_name](
            self._score_health_facility_definitions)
        score = scoring_function_instance.function(self)
        self.score_health_facility_type = score

        class_name = self._total_scoring_definitions['class_name']
        scoring_function_instance = generator_registry[class_name](
            self._total_scoring_definitions)
        score = scoring_function_instance.function(self)

        self.total_score_covid19 = score
        self.score_covid19_calculated = True
        self.update()

    def reset_score(self):
        # Reset scoring flag to False (need recalculate)
        self.score_covid19_calculated = False
        self.update()

    def is_score_calculated(self):
        return self.score_covid19_calculated
