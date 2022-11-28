import requests
import tenacity as tnc
from pydantic import dataclasses

from api_proxy.adapters.gateway import utils
from api_proxy.entities.country import Country
from api_proxy.entities.gateway import CountryGateway, CountryGatewayErrors


@dataclasses.dataclass
class HttpCountryGateway(CountryGateway):
    def __post_init_post_parse__(self):
        self._retry_strategy = {
            "stop": tnc.stop_after_attempt(3),
            "wait": tnc.wait_fixed(0.2),
            "retry": tnc.retry_if_exception_type(Exception),
            "reraise": True,
        }

    def get_country_name(self, country_id: str) -> Country:
        url = f"https://restcountries.com/v3.1/alpha/{country_id}"

        try:
            result = utils.retry(
                retry_strategy=self._retry_strategy,
                method=requests.get,
                url=url,
            )
            result.raise_for_status()
            name = result.json()[0]["name"]["official"]
            return Country(name=name)

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                raise CountryGatewayErrors.NotFoundError("Country not found") from err
            elif err.response.status_code == 422:
                raise CountryGatewayErrors.ValidationError("Validation error") from err
            raise CountryGatewayErrors.BaseError("unknown error") from err
