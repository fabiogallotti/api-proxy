import requests
import tenacity as tnc
from pydantic import dataclasses

from api_proxy.adapters.gateway import utils
from api_proxy.entities.gateway import NationalityGateway, NationalityGatewayErrors
from api_proxy.entities.nationality import Nationality


@dataclasses.dataclass
class HttpNationalityGateway(NationalityGateway):
    def __post_init_post_parse__(self):
        self._retry_strategy = {
            "stop": tnc.stop_after_attempt(3),
            "wait": tnc.wait_fixed(0.01),
            "retry": tnc.retry_if_exception_type(Exception),
            "reraise": True,
        }

    def get_nationality(self, name: str) -> Nationality:
        url = "https://api.nationalize.io"
        params = {"name": name}

        try:
            result = utils.retry(
                retry_strategy=self._retry_strategy,
                method=requests.get,
                url=url,
                params=params,
            )
            result.raise_for_status()
            return Nationality(**result.json())

        except requests.exceptions.HTTPError as err:
            if err.response.status_code == 404:
                raise NationalityGatewayErrors.NotFoundError("Nationality not found") from err
            elif err.response.status_code == 422:
                raise NationalityGatewayErrors.ValidationError("Validation error") from err
            raise NationalityGatewayErrors.BaseError("unknown error") from err
