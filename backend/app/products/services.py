from sqlalchemy.ext.asyncio import AsyncSession

from .crud import ProductsSet
from .schemas import Product
from .exceptions import ProductNotFound


class ProductsManager:

    def __init__(self, session: AsyncSession):
        self._products_set = ProductsSet(session)

    async def search(self, query: str = '', limit: int = 20) -> list[Product]:
        products = await self._products_set.search_products(query, limit)
        return [Product.model_validate(product) for product in products]

    async def get_all(self, ids: list[int] | None = None) -> list[Product]:
        if ids:
            ids_products = await self._products_set.get_by_ids(ids)
            return [Product.model_validate(product) for product in ids_products]

        all_products = await self._products_set.all()
        return [Product.model_validate(product) for product in all_products]

    async def get_concrete_or_none(self, id: int) -> Product | None:
        product = await self._products_set.get(id=id)
        return Product.model_validate(product) if product else None

    async def get_concrete(self, id: int) -> Product | None:
        product = await self._products_set.get(id=id)
        if not product:
            raise ProductNotFound(f"Product with id {id} doesn't exist")

        return Product.model_validate(product)

