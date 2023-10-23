from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateEatingProduct(BaseModel):
    id: int
    mass: float


class CreateEatingData(BaseModel):
    timestamp: datetime
    products: list[CreateEatingProduct]


class DbEatingProduct(BaseModel):
    id: int
    product_id: int
    mass: float

    model_config = ConfigDict(from_attributes=True)


class DbEating(BaseModel):
    id: int
    timestamp: datetime
    products: list[DbEatingProduct]

    model_config = ConfigDict(from_attributes=True)


class EatingProductResponse(BaseModel):
    id: int
    product_id: int
    mass: float


class EatingResponse(BaseModel):
    id: int
    timestamp: datetime
    products: list[EatingProductResponse]

