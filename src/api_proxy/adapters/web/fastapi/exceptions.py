import http
from typing import Dict, Optional

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .errors import JsonApiError, JsonApiErrors

__all__ = [
    "http_exception_handler",
    "request_validation_exception_handler",
    "unhandled_error_exception_handler",
]


def http_error_phrase(status_code: int) -> str:
    return http.HTTPStatus(status_code).phrase


def format_error_response(
    status: int, message: Optional[str] = None, code: Optional[str] = None
) -> Dict:
    error = JsonApiError(status=status, title=http_error_phrase(status), detail=message, code=code)
    return JsonApiErrors(errors=[error]).dict()


async def http_exception_handler(request, exc):
    status_code = exc.status_code or 500
    error_message = exc.detail or str(exc)
    error_content = format_error_response(status=status_code, message=error_message)
    return JSONResponse(content=jsonable_encoder(error_content), status_code=status_code)


async def request_validation_exception_handler(request, exc):
    status_code = 422
    try:
        error_message = "; ".join([err["msg"] for err in exc.errors()])
    except (AttributeError, IndexError):
        error_message = None
    error_message = error_message or "Request validation error"
    error_content = format_error_response(status=status_code, message=error_message)
    return JSONResponse(content=jsonable_encoder(error_content), status_code=status_code)


def unhandled_error_exception_handler():
    async def handler(request, exc):
        status_code = 500
        error_content = format_error_response(status=status_code, message="Something went wrong")
        return JSONResponse(content=jsonable_encoder(error_content), status_code=status_code)

    return handler
