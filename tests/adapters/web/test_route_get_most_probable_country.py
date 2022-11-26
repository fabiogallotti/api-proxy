import json

from api_proxy.adapters.web.fastapi import API_V1_PREFIX
from api_proxy.entities.country import MostProbableCountry


def test_returns_expected_country(client, mocker, controller):
    # given
    name = "fabio"
    expected_country = MostProbableCountry(name=name, message="msg")
    mocker.patch.object(controller, "get_most_probable_country", return_value=expected_country)
    # when
    response = client.get(f"{API_V1_PREFIX}/name/{name}")
    # then
    assert response.status_code == 200
    assert response.json()["data"] == json.loads(expected_country.json())
    controller.get_most_probable_country.assert_called_once_with(name=name)
