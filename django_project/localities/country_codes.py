"""ISO country-code helpers backed by Healthsites' source country data."""

import json
from functools import lru_cache
from pathlib import Path


COUNTRY_DATA = (
    Path(__file__).resolve().parent / 'data' / 'osm_boundaries' / 'country_data.json'
)


@lru_cache(maxsize=1)
def iso_3166_alpha2_to_alpha3():
    """Return the ISO alpha-2 to alpha-3 mapping used to seed Country."""
    with COUNTRY_DATA.open() as country_data:
        countries = json.load(country_data)

    return {
        country['Two_Letter_Country_Code'].upper():
        country['Three_Letter_Country_Code'].upper()
        for country in countries
        if country.get('Two_Letter_Country_Code') and
        country.get('Three_Letter_Country_Code')
    }


def get_iso_3166_alpha3(country_code):
    """Return the alpha-3 equivalent for an ISO alpha-2 country code."""
    if not isinstance(country_code, str):
        return None
    return iso_3166_alpha2_to_alpha3().get(country_code.strip().upper())
