from sqlalchemy import select
from sqlalchemy.dialects.postgresql.ext import plainto_tsquery
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


class ProductsSet:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def search_products(self, query: str = '', limit: int = 20) -> list[Product]:
        stmt = select(Product).where(
            Product.title_vector.op('@@')(plainto_tsquery(query))
        ).order_by(
            func.ts_rank(Product.title_vector, plainto_tsquery(query)).desc()
        ).limit(limit)
        result = await self._session.execute(stmt)
        products = result.scalars().all()
        return list(products)

    async def get(self, id: int) -> Product | None:
        stmt = select(Product).where(Product.id == id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def all(self) -> list[Product]:
        stmt = select(Product)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_ids(self, ids: list[int]) -> list[Product]:
        stmt = select(Product).where(Product.id.in_(ids))
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

