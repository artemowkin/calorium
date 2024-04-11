from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    per_page: int
    pages_count: int
    total: int
    data: list[T]
