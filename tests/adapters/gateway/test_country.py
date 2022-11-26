import pytest
import responses

from api_proxy.adapters.gateway.country import HttpCountryGateway
from api_proxy.entities.country import Country

COUNTRY_EXAMPLE_RESPONSE = [
    {
        "name": {
            "common": "Germany",
            "official": "Federal Republic of Germany",
            "nativeName": {
                "deu": {"official": "Bundesrepublik Deutschland", "common": "Deutschland"}
            },
        },
        "tld": [".de"],
        "cca2": "DE",
        "ccn3": "276",
        "cca3": "DEU",
        "cioc": "GER",
        "independent": True,
        "status": "officially-assigned",
        "unMember": True,
        "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
        "idd": {"root": "+4", "suffixes": ["9"]},
        "capital": ["Berlin"],
        "altSpellings": ["DE", "Federal Republic of Germany", "Bundesrepublik Deutschland"],
        "region": "Europe",
        "subregion": "Western Europe",
        "languages": {"deu": "German"},
        "translations": {
            "ara": {"official": "جمهورية ألمانيا الاتحادية", "common": "ألمانيا"},
            "bre": {"official": "Republik Kevreadel Alamagn", "common": "Alamagn"},
            "ces": {"official": "Spolková republika Německo", "common": "Německo"},
            "cym": {"official": "Federal Republic of Germany", "common": "Germany"},
            "deu": {"official": "Bundesrepublik Deutschland", "common": "Deutschland"},
            "est": {"official": "Saksamaa Liitvabariik", "common": "Saksamaa"},
            "fin": {"official": "Saksan liittotasavalta", "common": "Saksa"},
            "fra": {"official": "République fédérale d'Allemagne", "common": "Allemagne"},
            "hrv": {"official": "Njemačka Federativna Republika", "common": "Njemačka"},
            "hun": {"official": "Német Szövetségi Köztársaság", "common": "Németország"},
            "ita": {"official": "Repubblica federale di Germania", "common": "Germania"},
            "jpn": {"official": "ドイツ連邦共和国", "common": "ドイツ"},
            "kor": {"official": "독일 연방 공화국", "common": "독일"},
            "nld": {"official": "Bondsrepubliek Duitsland", "common": "Duitsland"},
            "per": {"official": "جمهوری فدرال آلمان", "common": "آلمان"},
            "pol": {"official": "Republika Federalna Niemiec", "common": "Niemcy"},
            "por": {"official": "República Federal da Alemanha", "common": "Alemanha"},
            "rus": {"official": "Федеративная Республика Германия", "common": "Германия"},
            "slk": {"official": "Nemecká spolková republika", "common": "Nemecko"},
            "spa": {"official": "República Federal de Alemania", "common": "Alemania"},
            "swe": {"official": "Förbundsrepubliken Tyskland", "common": "Tyskland"},
            "tur": {"official": "Almanya Federal Cumhuriyeti", "common": "Almanya"},
            "urd": {"official": "وفاقی جمہوریہ جرمنی", "common": "جرمنی"},
            "zho": {"official": "德意志联邦共和国", "common": "德国"},
        },
        "latlng": [51.0, 9.0],
        "landlocked": False,
        "borders": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"],
        "area": 357114.0,
        "demonyms": {
            "eng": {"f": "German", "m": "German"},
            "fra": {"f": "Allemande", "m": "Allemand"},
        },
        "flag": "\uD83C\uDDE9\uD83C\uDDEA",
        "maps": {
            "googleMaps": "https://goo.gl/maps/mD9FBMq1nvXUBrkv6",
            "openStreetMaps": "https://www.openstreetmap.org/relation/51477",
        },
        "population": 83240525,
        "gini": {"2016": 31.9},
        "fifa": "GER",
        "car": {"signs": ["DY"], "side": "right"},
        "timezones": ["UTC+01:00"],
        "continents": ["Europe"],
        "flags": {"png": "https://flagcdn.com/w320/de.png", "svg": "https://flagcdn.com/de.svg"},
        "coatOfArms": {
            "png": "https://mainfacts.com/media/images/coats_of_arms/de.png",
            "svg": "https://mainfacts.com/media/images/coats_of_arms/de.svg",
        },
        "startOfWeek": "monday",
        "capitalInfo": {"latlng": [52.52, 13.4]},
        "postalCode": {"format": "#####", "regex": "^(\\d{5})$"},
    }
]


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def gateway():
    return HttpCountryGateway()


def test_does_correct_http_request(gateway, mocked_responses):
    # given
    country_id = "de"
    url = f"https://restcountries.com/v3.1/alpha/{country_id}"
    mocked_responses.add(responses.GET, url, json=COUNTRY_EXAMPLE_RESPONSE, status=200)
    # when
    result = gateway.get_country_name(country_id=country_id)
    # then
    assert result == Country(name=COUNTRY_EXAMPLE_RESPONSE[0]["name"]["official"])
