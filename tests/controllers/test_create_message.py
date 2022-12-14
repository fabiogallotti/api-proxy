import pytest

from tests import factories as fty


@pytest.mark.parametrize(
    "nationality,expected_msg",
    [
        pytest.param(
            fty.NationalityFactory(
                name="fabio",
                country=[fty.NationalityCountryFactory(country_id="it", probability=0.9)],
            ),
            "fabio is mostly certain from Italia",
            id="x>0.7",
        ),
        pytest.param(
            fty.NationalityFactory(
                name="fabio",
                country=[fty.NationalityCountryFactory(country_id="it", probability=0.4)],
            ),
            "fabio may be from Italia",
            id="0.3<=x<=0.7",
        ),
        pytest.param(
            fty.NationalityFactory(
                name="fabio",
                country=[fty.NationalityCountryFactory(country_id="it", probability=0.1)],
            ),
            "It seems that fabio is from Italia. But I'm just guessing!",
            id="x<0.3",
        ),
    ],
)
def test_create_message(controller, nationality, expected_msg):
    # given
    country_name = "Italia"
    # when
    res = controller._create_message(nationality=nationality, country_name=country_name)
    # then
    assert res == expected_msg
