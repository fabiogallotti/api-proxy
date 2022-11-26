import requests
from pydantic import dataclasses

from api_proxy.entities.gateway import NationalityGateway
from api_proxy.entities.nationality import Nationality


@dataclasses.dataclass
class HttpNationalityGateway(NationalityGateway):
    def get_nationality(self, name: str) -> Nationality:
        url = "https://api.nationalize.io"
        params = {"name": name}

        result = requests.get(url=url, params=params)

        return Nationality(**result.json())
