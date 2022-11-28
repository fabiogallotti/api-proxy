import abc

from api_proxy.entities.country import Country
from api_proxy.entities.nationality import Nationality


class NationalityGatewayErrors:
    class BaseError(Exception):
        pass

    class NotFoundError(BaseError):
        pass

    class ValidationError(BaseError):
        pass


class NationalityGateway(abc.ABC):
    def get_nationality(self, name: str) -> Nationality:
        raise NotImplementedError("NationalityGateway.get_nationality")  # pragma: no cover


class CountryGatewayErrors:
    class BaseError(Exception):
        pass

    class NotFoundError(BaseError):
        pass

    class ValidationError(BaseError):
        pass


class CountryGateway(abc.ABC):
    def get_country_name(self, country_id: str) -> Country:
        raise NotImplementedError("CountryGateway.get_country_name")  # pragma: no cover
