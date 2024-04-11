from app.auth.schemas import DbUser
from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    id: int
    title: str
    kkal: float
    file_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateProductModel(BaseModel):
    title: str
    kkal: float
    owner: DbUser
    file_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CreateProductData(BaseModel):
    title: str
    kkal: float
