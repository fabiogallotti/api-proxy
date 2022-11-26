import pytest

from api_proxy.controllers import Controller


@pytest.fixture(autouse=True)
def http_nationality_gateway(mocker):
    return mocker.patch("api_proxy.controllers.HttpNationalityGateway", autospec=True)


@pytest.fixture(autouse=True)
def http_country_gateway(mocker):
    return mocker.patch("api_proxy.controllers.HttpCountryGateway", autospec=True)


@pytest.fixture
def controller():
    return Controller()
