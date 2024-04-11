from app.auth.schemas import DbUser
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Eating, EatingProduct
from .schemas import CreateEatingData, DbEating


class EatingsQueries:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, data: CreateEatingData, user: DbUser) -> DbEating:
        stmt = insert(Eating).returning(Eating.id).values(timestamp=data.timestamp, user_id=user.id)
        result = await self._session.execute(stmt)
        eating_id = result.scalar_one()
        stmt = insert(EatingProduct).values(
            [
                {
                    "product_id": product.id,
                    "eating_id": eating_id,
                    "mass": product.mass,
                }
                for product in data.products
            ]
        )
        await self._session.execute(stmt)
        stmt = select(Eating).options(selectinload(Eating.products)).where(Eating.id == eating_id)
        result = await self._session.execute(stmt)
        created_eating = result.scalar_one()
        return DbEating.model_validate(created_eating)

    async def get_all(self, user: DbUser) -> list[DbEating]:
        stmt = select(Eating).where(Eating.user_id == user.id).options(selectinload(Eating.products))
        result = await self._session.execute(stmt)
        print(stmt)
        eatings = result.scalars().all()
        print(eatings)
        return [DbEating.model_validate(eating) for eating in eatings]
