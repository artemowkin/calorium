import math
from typing import TypeVar

from app.auth.schemas import DbUser
from app.utils.schemas import PaginatedResponse
from sqlalchemy import Select, func, insert, select
from sqlalchemy.dialects.postgresql import to_tsvector
from sqlalchemy.dialects.postgresql.ext import plainto_tsquery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import func

from .models import Product
from .schemas import CreateProductModel
from .schemas import Product as ProductModel

T = TypeVar("T")


class ProductsSet:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def search_products(self, query: str = "", limit: int = 20) -> list[Product]:
        stmt = (
            select(Product)
            .where(Product.title_vector.op("@@")(plainto_tsquery(query)))
            .order_by(func.ts_rank(Product.title_vector, plainto_tsquery(query)).desc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        products = result.scalars().all()
        return list(products)

    async def get(self, id: int) -> Product | None:
        stmt = select(Product).where(Product.id == id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    def _filter_products_stmt(
        self, stmt: Select[tuple[T]], ids: list[int] | None = None, owner: DbUser | None = None
    ) -> Select[tuple[T]]:
        if ids:
            stmt = stmt.where(Product.id.in_(ids))
        if owner:
            stmt = stmt.where(Product.owner_id == owner.id)
        else:
            stmt = stmt.where(Product.owner_id == None)

        return stmt

    def _validate_page_per_page(self, page: int, per_page: int, pages_count: int) -> tuple[int, int]:
        if page > pages_count:
            page = pages_count
        if page <= 0:
            page = 1

        if per_page <= 0:
            per_page = 50

        return page, per_page

    async def _get_products_count(self, ids: list[int] | None = None, owner: DbUser | None = None) -> int:
        count_stmt = select(func.count()).select_from(Product)
        filtered_count_stmt = self._filter_products_stmt(count_stmt, ids, owner)
        count_result = await self._session.execute(filtered_count_stmt)
        products_count = count_result.scalar() or 0
        return products_count

    async def _get_paginated_products(
        self, offset: int, per_page: int, ids: list[int] | None = None, owner: DbUser | None = None
    ) -> list[ProductModel]:
        result_stmt = select(Product)
        filtered_result_stmt = self._filter_products_stmt(result_stmt, ids, owner)
        paginated_result_stmt = filtered_result_stmt.offset(offset).limit(per_page)
        result = await self._session.execute(paginated_result_stmt)
        result_products = result.scalars().all()
        return [ProductModel.model_validate(p) for p in result_products]

    async def all(
        self, page: int = 1, per_page: int = 50, ids: list[int] | None = None, owner: DbUser | None = None
    ) -> PaginatedResponse[ProductModel]:
        products_count = await self._get_products_count(ids, owner)
        pages_count = math.ceil(products_count / per_page)
        page, per_page = self._validate_page_per_page(page, per_page, pages_count)
        offset = (page - 1) * per_page
        result_products = await self._get_paginated_products(offset, per_page, ids, owner)
        return PaginatedResponse(
            page=page,
            per_page=per_page,
            pages_count=pages_count,
            total=products_count,
            data=result_products,
        )

    async def get_by_ids(self, ids: list[int]) -> list[Product]:
        stmt = select(Product).where(Product.id.in_(ids))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, product: CreateProductModel) -> ProductModel:
        stmt = (
            insert(Product)
            .values(
                **product.model_dump(exclude={"owner"}),
                owner_id=product.owner.id,
                title_vector=to_tsvector(product.title),
            )
            .returning(Product)
        )
        result = await self._session.execute(stmt)
        created_product = result.scalar_one()
        return ProductModel.model_validate(created_product)
