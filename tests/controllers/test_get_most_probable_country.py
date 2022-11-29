from api_proxy.entities.country import Country, MostProbableCountry
from tests import factories as fty


def test_get_most_probable_country(controller):
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
    country = Country(name="Italia")
    controller.nationality_gateway.get_nationality.return_value = nationality
    controller.country_gateway.get_country_name.return_value = country
    # when
    result = controller.get_most_probable_country(name=name)
    # then
    assert isinstance(result, MostProbableCountry)
    assert result.name == "fabio"
    assert result.message == "fabio is mostly certain from Italia"
