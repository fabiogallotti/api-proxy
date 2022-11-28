from typing import Optional

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from api_proxy.controllers import Controller

from .endpoints import router
from .exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
    unhandled_error_exception_handler,
)

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

    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_error_exception_handler)

    add_healthcheck_api(app, config.version)

    app.include_router(router(controller=controller), prefix=API_V1_PREFIX)

    return app
