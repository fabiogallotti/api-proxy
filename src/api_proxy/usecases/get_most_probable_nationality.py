from typing import Any

from api_proxy.entities.gateway import NationalityGateway
from api_proxy.entities.nationality import Nationality
from api_proxy.usecases import common


class GetMostProbableNationalityError:
    class BaseError(Exception):
        pass

    class NoCountryFound(BaseError):
        pass


class UsecaseEnv(common.UsecaseEnv):
    logger: Any
    nationality_gateway: NationalityGateway


class UsecaseReq(common.UsecaseReq):
    name: str


class Usecase(common.Usecase):
    env: UsecaseEnv

    def execute(self, req: UsecaseReq) -> Nationality:
        nationality = self.env.nationality_gateway.get_nationality(name=req.name)
        sorted_countries = sorted(nationality.country, key=lambda x: x.probability, reverse=True)

        try:
            most_probable_country = sorted_countries[0]
            return Nationality(name=nationality.name, country=[most_probable_country])
        except IndexError as err:
            raise GetMostProbableNationalityError.NoCountryFound("no country found") from err
