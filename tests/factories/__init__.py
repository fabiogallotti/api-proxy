from random import uniform

import factory

from api_proxy.entities.nationality import Nationality, NationalityCountry


class NationalityCountryFactory(factory.Factory):
    country_id = factory.Faker("country_code")
    probability = factory.LazyFunction(lambda: uniform(0.0, 1.0))

    class Meta:
        model = NationalityCountry


class NationalityFactory(factory.Factory):
    name = factory.Sequence(lambda n: f"name-{n}")
    country = factory.LazyAttribute(
        lambda n: [NationalityCountryFactory() for _ in range(n.country_number)]
    )

    class Params:
        country_number = 3

    class Meta:
        model = Nationality
