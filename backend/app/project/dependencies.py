from sqlalchemy.ext.asyncio import AsyncSession

from .db import session


async def use_session() -> AsyncSession:
    async with session() as s:
        yield s
        await s.commit()

