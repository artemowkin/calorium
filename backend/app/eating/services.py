from app.auth.schemas import DbUser
from sqlalchemy.ext.asyncio import AsyncSession

from ..products.services import ProductsManager
from .crud import EatingsQueries
from .schemas import CreateEatingData, DateStatistic, DbEating


class EatingsManager:

    def __init__(self, session: AsyncSession):
        self._session = session
        self._eatings_queries = EatingsQueries(session)
        self._products_manager = ProductsManager(session)

    async def create(self, data: CreateEatingData, user: DbUser) -> DbEating:
        for product in data.products:
            product = await self._products_manager.get_concrete(product.id)

        eating = await self._eatings_queries.create(data, user)
        return eating

    async def all(self, user: DbUser) -> list[DbEating]:
        all_eatings = await self._eatings_queries.get_all(user)
        return all_eatings

    async def get_statistics(self, user: DbUser, start_month: str, end_month: str) -> list[DateStatistic]:
        statistics = await self._eatings_queries.get_statistics(user, start_month, end_month)
        return statistics
