import pytest
import responses

from api_proxy.adapters.gateway.nationality import HttpNationalityGateway
from api_proxy.entities.nationality import Nationality

NATIONALITY_EXAMPLE_RESPONSE = {
    "country": [
        {"country_id": "AT", "probability": 0.064},
        {"country_id": "DE", "probability": 0.059},
        {"country_id": "DK", "probability": 0.058},
        {"country_id": "IE", "probability": 0.051},
        {"country_id": "AU", "probability": 0.047},
    ],
    "name": "michael",
}


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def gateway():
    return HttpNationalityGateway()


def test_does_correct_http_request(gateway, mocked_responses):
    # given
    url = "https://api.nationalize.io"
    mocked_responses.add(responses.GET, url, json=NATIONALITY_EXAMPLE_RESPONSE, status=200)
    # when
    result = gateway.get_nationality(name="michael")
    # then
    assert result == Nationality(**NATIONALITY_EXAMPLE_RESPONSE)
