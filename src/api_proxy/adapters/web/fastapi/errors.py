from typing import List, Optional

from pydantic import BaseModel, Extra, Field


class JsonApiError(BaseModel):
    status: Optional[int] = Field(
        None,
        description="HTTP status code.",
    )
    title: Optional[str] = Field(
        None,
        description="Short, human-readable summary of the problem type.",
    )
    detail: Optional[str] = Field(
        None,
        description="Human-readable explanation specific to the problem.",
    )
    code: Optional[str] = Field(
        None,
        description="Application-specific error code.",
    )

    class Config:
        extra = Extra.forbid


class JsonApiErrors(BaseModel):
    errors: List[JsonApiError]

    class Config:
        extra = Extra.forbid
