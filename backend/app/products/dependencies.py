from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .services import ProductsManager
from ..project.dependencies import use_session


async def use_products_manager(session: Annotated[AsyncSession, Depends(use_session)]) -> ProductsManager:
    return ProductsManager(session)
