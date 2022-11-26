from pydantic import BaseModel


class Country(BaseModel):
    name: str


class MostProbableCountry(BaseModel):
    name: str
    message: str
