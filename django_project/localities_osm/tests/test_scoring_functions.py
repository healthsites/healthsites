# coding=utf-8

from django.test import TestCase
from localities_osm.models.locality import LocalityOSM


class ScoringFunctionTest(TestCase):

    def setUp(self):
        # Prepare rows of osm locality data
        pass

    def test_scoring_functions(self):
        expected_value = {
            'total_score_covid19': 4,
            'score_health_facility_type': 2,
        }

        # get just one row
        row = LocalityOSM.objects.first()
        """:type: LocalityOSM"""

        row.calculate_score()
        row.refresh_from_db()

        actual_value = {}
        for key, value in expected_value.items():
            actual_value[key] = getattr(row, key)

        self.assertEqual(expected_value, actual_value)
