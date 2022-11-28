from fastapi import APIRouter, HTTPException, Path
from fastapi.routing import APIRoute
from pydantic import BaseModel

from api_proxy.controllers import Controller
from api_proxy.entities.country import MostProbableCountry
from api_proxy.entities.gateway import CountryGatewayErrors, NationalityGatewayErrors
from api_proxy.usecases.get_most_probable_nationality import GetMostProbableNationalityError

from .errors import JsonApiErrors


class MostProbableCountryResponse(BaseModel):
    data: MostProbableCountry


def route_get_most_probable_country(controller: Controller):
    def endpoint(
        name: str = Path(..., description="the person given name")
    ) -> MostProbableCountryResponse:
        try:
            res = controller.get_most_probable_country(name=name)
            return MostProbableCountryResponse(data=res)
        except NationalityGatewayErrors.NotFoundError:
            raise HTTPException(status_code=404, detail="Nationality not found")
        except (CountryGatewayErrors.NotFoundError, GetMostProbableNationalityError.NoCountryFound):
            raise HTTPException(status_code=404, detail="Country not found")

    return APIRoute(
        path="/name/{name}",
        endpoint=endpoint,
        status_code=200,
        response_model=MostProbableCountryResponse,
        methods=["GET"],
        summary="Get most probable country of the given name",
        response_description="Returns the given name and the most probable country in a message",
        responses={
            400: {"model": JsonApiErrors, "description": "Malformed cursor."},
            403: {"model": JsonApiErrors, "description": "Forbidden."},
            422: {"model": JsonApiErrors, "description": "Validation Error."},
            500: {"model": JsonApiErrors, "description": "Internal server error."},
        },
    )


def router(controller: Controller):
    return APIRouter(routes=[route_get_most_probable_country(controller)])
