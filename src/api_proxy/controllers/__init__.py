from pydantic import dataclasses

from api_proxy.adapters.gateway.country import HttpCountryGateway
from api_proxy.adapters.gateway.nationality import HttpNationalityGateway
from api_proxy.entities.country import MostProbableCountry
from api_proxy.entities.nationality import Nationality
from api_proxy.usecases import get_most_probable_nationality


@dataclasses.dataclass
class Controller:
    def __post_init_post_parse__(self):
        self.nationality_gateway = HttpNationalityGateway()
        self.country_gateway = HttpCountryGateway()

    def get_most_probable_country(self, name: str) -> MostProbableCountry:
        env = get_most_probable_nationality.UsecaseEnv(
            nationality_gateway=self.nationality_gateway,
        )
        req = get_most_probable_nationality.UsecaseReq(name=name)
        most_probable_nationality = get_most_probable_nationality.Usecase(env=env).execute(req=req)

        country_name = self.country_gateway.get_country_name(
            country_id=most_probable_nationality.country[0].country_id
        )
        message = self._create_message(
            nationality=most_probable_nationality, country_name=country_name.name
        )

        return MostProbableCountry(name=most_probable_nationality.name, message=message)

    def _create_message(self, nationality: Nationality, country_name: str) -> str:
        if nationality.country[0].probability > 0.6:
            return f"{nationality.name} is mostly certain from {country_name}"
        elif 0.3 <= nationality.country[0].probability <= 0.6:
            return f"{nationality.name} may be from {country_name}"
        else:
            return (
                f"It seems that {nationality.name} is from {country_name}. But I'm just guessing!"
            )
