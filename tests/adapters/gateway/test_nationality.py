import json

import pytest
import responses

from api_proxy.adapters.gateway.nationality import HttpNationalityGateway
from api_proxy.entities.gateway import NationalityGatewayErrors
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


@pytest.mark.parametrize(
    "status,body,exception,expected_calls",
    [
        pytest.param(
            404,
            json.dumps(
                {
                    "errors": [
                        {
                            "status": "404",
                            "title": "Not Found",
                        }
                    ]
                }
            ),
            NationalityGatewayErrors.NotFoundError,
            1,
        ),
        pytest.param(
            422,
            json.dumps(
                {
                    "errors": [
                        {
                            "status": "422",
                            "title": "Validation Error",
                        }
                    ]
                }
            ),
            NationalityGatewayErrors.ValidationError,
            1,
        ),
        pytest.param(
            500,
            json.dumps(
                {
                    "errors": [
                        {
                            "status": "500",
                            "title": "Internal Server Error",
                        }
                    ]
                }
            ),
            NationalityGatewayErrors.BaseError,
            3,
        ),
    ],
)
def test_raises_if_errors(gateway, mocked_responses, status, body, exception, expected_calls):
    url = "https://api.nationalize.io"
    mocked_responses.add(
        responses.GET,
        url,
        body=body,
        status=status,
        content_type="application/json",
    )
    with pytest.raises(exception):
        gateway.get_nationality(name="michael")

    assert len(mocked_responses.calls) == expected_calls
