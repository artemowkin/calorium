from typing import Annotated
from fastapi import APIRouter, Depends

from .schemas import EatingResponse, CreateEatingData
from .dependencies import use_eatings_manager
from .services import EatingsManager
from ..auth.dependencies import auth_required
from ..auth.schemas import DbUser


router = APIRouter()


@router.post('/', response_model=EatingResponse)
async def create_eating(request: CreateEatingData,
                        user: Annotated[DbUser, Depends(auth_required)],
                        eatings_manager: Annotated[EatingsManager, Depends(use_eatings_manager)]):
    created_eating = await eatings_manager.create(request, user)
    return created_eating


@router.get('/', response_model=list[EatingResponse])
async def all_eatings(user: Annotated[DbUser, Depends(auth_required)],
                      eatings_manager: Annotated[EatingsManager, Depends(use_eatings_manager)]):
    all_eatings = await eatings_manager.all(user)
    return all_eatings

