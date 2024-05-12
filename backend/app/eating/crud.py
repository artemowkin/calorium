from datetime import datetime
from zoneinfo import ZoneInfo

from app.auth.schemas import DbUser
from dateutil.relativedelta import relativedelta
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, lazyload, selectinload

from .models import Eating, EatingProduct
from .schemas import CreateEatingData, DateStatistic, DbEating


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
        eatings = result.scalars().all()
        return [DbEating.model_validate(eating) for eating in eatings]

    async def get_statistics(self, user: DbUser, start_month: str, end_month: str) -> list[DateStatistic]:
        start_month_datetime = datetime.fromisoformat(f"{start_month}-01T00:00:00").astimezone(ZoneInfo("UTC"))
        end_month_datetime = datetime.fromisoformat(f"{end_month}-01T00:00:00").astimezone(ZoneInfo("UTC"))
        stmt = (
            select(Eating)
            .options(joinedload(Eating.products).subqueryload(EatingProduct.product))
            .where(
                Eating.user_id == user.id,
                Eating.timestamp >= start_month_datetime,
                Eating.timestamp < end_month_datetime,
            )
        )
        result = await self._session.execute(stmt)
        eatings = result.scalars().unique().all()
        date_kkals: list[DateStatistic] = []
        dateobj = start_month_datetime.date()
        while dateobj < end_month_datetime.date():
            date_eatings = [e for e in eatings if e.timestamp.date() == dateobj]
            total_date_kkals = 0
            for eating in date_eatings:
                eating_total_mass = sum([(ep.mass * ep.product.kkal) / 100 for ep in eating.products])
                total_date_kkals += eating_total_mass

            date_kkals.append(DateStatistic(date=dateobj, total_kkals=round(total_date_kkals)))
            dateobj = dateobj + relativedelta(days=1)

        return date_kkals
