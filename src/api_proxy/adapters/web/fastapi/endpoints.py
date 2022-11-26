from fastapi import APIRouter, HTTPException, Path
from fastapi.routing import APIRoute
from pydantic import BaseModel

from api_proxy.controllers import Controller
from api_proxy.entities.country import MostProbableCountry


class MostProbableCountryResponse(BaseModel):
    data: MostProbableCountry


def route_get_most_probable_country(controller: Controller):
    def endpoint(
        name: str = Path(..., description="the person given name")
    ) -> MostProbableCountryResponse:
        try:
            res = controller.get_most_probable_country(name=name)
            return MostProbableCountryResponse(data=res)
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    return APIRoute(
        path="/name/{name}",
        endpoint=endpoint,
        status_code=200,
        response_model=MostProbableCountryResponse,
        methods=["GET"],
        summary="Get most probable country of the given name",
        response_description="Returns the given name and the most probable country in a message",
    )


def router(controller: Controller):
    return APIRouter(routes=[route_get_most_probable_country(controller)])
