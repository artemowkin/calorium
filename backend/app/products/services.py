from app.auth.schemas import DbUser
from app.utils.schemas import PaginatedResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import ProductsSet
from .exceptions import ProductNotFound
from .schemas import CreateProductModel, Product


class ProductsManager:

    def __init__(self, session: AsyncSession):
        self._products_set = ProductsSet(session)

    async def search(self, query: str = "", limit: int = 20) -> list[Product]:
        products = await self._products_set.search_products(query, limit)
        return [Product.model_validate(product) for product in products]

    async def get_all(
        self, page: int = 1, per_page: int = 50, ids: list[int] | None = None, owner: DbUser | None = None
    ) -> PaginatedResponse[Product]:
        all_products = await self._products_set.all(page, per_page, ids, owner)
        return all_products

    async def get_concrete_or_none(self, id: int) -> Product | None:
        product = await self._products_set.get(id=id)
        return Product.model_validate(product) if product else None

    async def get_concrete(self, id: int) -> Product | None:
        product = await self._products_set.get(id=id)
        if not product:
            raise ProductNotFound(f"Product with id {id} doesn't exist")

        return Product.model_validate(product)

    async def create(self, product: CreateProductModel) -> Product:
        created_product = await self._products_set.create(product)
        return created_product
