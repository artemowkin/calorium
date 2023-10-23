from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .services import EatingsManager
from ..project.dependencies import use_session


def use_eatings_manager(session: Annotated[AsyncSession, Depends(use_session)]) -> EatingsManager:
    return EatingsManager(session)
