from pydantic import BaseModel, ConfigDict


class Product(BaseModel):
    id: int
    title: str
    kkal: float
    file_url: str | None = None

    model_config = ConfigDict(from_attributes=True)

