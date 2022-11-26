import abc

from api_proxy.entities.country import Country
from api_proxy.entities.nationality import Nationality


class NationalityGateway(abc.ABC):
    def get_nationality(self, name: str) -> Nationality:
        raise NotImplementedError("NationalityGateway.get_nationality")  # pragma: no cover


class CountryGateway(abc.ABC):
    def get_country_name(self, country_id: str) -> Country:
        raise NotImplementedError("CountryGateway.get_country_name")  # pragma: no cover
