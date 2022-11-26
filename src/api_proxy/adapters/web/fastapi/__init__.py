from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from api_proxy.controllers import Controller

from .endpoints import router

API_V1_PREFIX = "/api/v1"


class WebApiConfig(BaseModel):
    title: str
    version: str
    root_path: Optional[str] = None


def add_healthcheck_api(app: FastAPI, version: str):
    class HealthResponse(BaseModel):
        version: str

    def handler():
        return {"version": version}

    app.add_api_route(
        path="/health",
        endpoint=handler,
        summary="Health check",
        response_model=HealthResponse,
    )


def create_app(controller: Controller, config: WebApiConfig) -> FastAPI:
    app = FastAPI(title=config.title, version=config.version, root_path=config.root_path or "")

    add_healthcheck_api(app, config.version)

    app.include_router(router(controller=controller), prefix=API_V1_PREFIX)

    return app
