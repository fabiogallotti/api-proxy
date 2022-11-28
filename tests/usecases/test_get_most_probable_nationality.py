import pytest

from api_proxy.entities.gateway import NationalityGateway
from api_proxy.usecases.get_most_probable_nationality import (
    GetMostProbableNationalityError,
    Usecase,
    UsecaseEnv,
    UsecaseReq,
)
from tests import factories as fty


@pytest.fixture
def nationality_gateway(mocker):
    return mocker.Mock(spec=NationalityGateway)


@pytest.fixture
def env(nationality_gateway):
    return UsecaseEnv(
        nationality_gateway=nationality_gateway,
    )


def test_get_most_probable_nationality(env, nationality_gateway):
    # given
    name = "fabio"
    nationality = fty.NationalityFactory(
        name=name,
        country=[
            fty.NationalityCountryFactory(country_id="de", probability="0.01"),
            fty.NationalityCountryFactory(country_id="fr", probability="0.1"),
            fty.NationalityCountryFactory(country_id="it", probability="0.9"),
        ],
    )
    nationality_gateway.get_nationality.return_value = nationality

    expected_nationality = fty.NationalityFactory(
        name=name,
        country=[
            fty.NationalityCountryFactory(country_id="it", probability="0.9"),
        ],
    )
    # when
    req = UsecaseReq(name=name)
    res = Usecase(env=env).execute(req=req)
    # then
    assert res == expected_nationality
    nationality_gateway.get_nationality.assert_called_once_with(name=name)


def test_raises_for_no_country(env, nationality_gateway):
    # given
    name = "fabio"
    nationality = fty.NationalityFactory(name=name, country=[])
    nationality_gateway.get_nationality.return_value = nationality
    # when
    req = UsecaseReq(name=name)
    with pytest.raises(GetMostProbableNationalityError.NoCountryFound):
        Usecase(env=env).execute(req=req)
    # then
    nationality_gateway.get_nationality.assert_called_once()
