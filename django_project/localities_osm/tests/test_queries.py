from unittest.mock import call, patch

from django.test import SimpleTestCase

from localities.models import Country
from localities_osm.queries import get_country


class CountryQueryTests(SimpleTestCase):

    @patch.object(Country.objects, 'get')
    def test_resolves_alpha2_code_to_seeded_alpha3_country(self, mock_get):
        country = object()
        mock_get.side_effect = [Country.DoesNotExist, country]

        self.assertIs(get_country('us'), country)
        self.assertEqual(
            mock_get.call_args_list,
            [call(name__iexact='us'), call(code__iexact='USA')]
        )

    @patch.object(Country.objects, 'get')
    def test_resolves_alpha3_code_to_seeded_country(self, mock_get):
        country = object()
        mock_get.side_effect = [Country.DoesNotExist, country]

        self.assertIs(get_country('nzl'), country)
        self.assertEqual(
            mock_get.call_args_list,
            [call(name__iexact='nzl'), call(code__iexact='NZL')]
        )
