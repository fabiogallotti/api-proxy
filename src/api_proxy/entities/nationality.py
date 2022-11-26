from typing import List

from pydantic import BaseModel


class NationalityCountry(BaseModel):
    country_id: str
    probability: float


class Nationality(BaseModel):
    name: str
    country: List[NationalityCountry]
