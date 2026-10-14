from django.test import SimpleTestCase

from localities.country_codes import get_iso_3166_alpha3


class CountryCodeTests(SimpleTestCase):

    def test_resolves_alpha2_codes_case_insensitively(self):
        self.assertEqual(get_iso_3166_alpha3('us'), 'USA')
        self.assertEqual(get_iso_3166_alpha3(' NZ '), 'NZL')

    def test_returns_none_for_codes_not_in_the_source_data(self):
        self.assertIsNone(get_iso_3166_alpha3('ZZ'))
        self.assertIsNone(get_iso_3166_alpha3(None))
