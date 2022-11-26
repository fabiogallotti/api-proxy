from api_proxy.entities.gateway import NationalityGateway
from api_proxy.entities.nationality import Nationality
from api_proxy.usecases import common


class UsecaseEnv(common.UsecaseEnv):
    nationality_gateway: NationalityGateway


class UsecaseReq(common.UsecaseReq):
    name: str


class Usecase(common.Usecase):
    env: UsecaseEnv

    def execute(self, req: UsecaseReq) -> Nationality:
        nationality = self.env.nationality_gateway.get_nationality(name=req.name)

        sorted_countries = sorted(nationality.country, key=lambda x: x.probability, reverse=True)
        most_probable_country = sorted_countries[0]

        return Nationality(name=nationality.name, country=[most_probable_country])
