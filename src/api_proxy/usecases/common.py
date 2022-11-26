from typing import Any

from pydantic import BaseModel, Extra

UsecaseResult = Any


class UsecaseEnv(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.forbid


class UsecaseReq(BaseModel):
    class Config:
        extra = Extra.forbid


class Usecase(BaseModel):
    env: UsecaseEnv

    def execute(self, req: UsecaseReq) -> UsecaseResult:
        raise NotImplementedError("not implemented")  # pragma: no cover
