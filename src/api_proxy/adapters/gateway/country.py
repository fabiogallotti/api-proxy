import requests
from pydantic import dataclasses

from api_proxy.entities.country import Country
from api_proxy.entities.gateway import CountryGateway


@dataclasses.dataclass
class HttpCountryGateway(CountryGateway):
    def get_country_name(self, country_id: str) -> Country:
        url = f"https://restcountries.com/v3.1/alpha/{country_id}"

        result = requests.get(url=url)
        name = result.json()[0]["name"]["official"]
        return Country(name=name)
