from datetime import date
from typing import Annotated

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Query

from ..auth.dependencies import auth_required
from ..auth.schemas import DbUser
from .dependencies import use_eatings_manager
from .schemas import CreateEatingData, DateStatistic, EatingResponse
from .services import EatingsManager

router = APIRouter()


@router.post("/", response_model=EatingResponse)
async def create_eating(
    request: CreateEatingData,
    user: Annotated[DbUser, Depends(auth_required)],
    eatings_manager: Annotated[EatingsManager, Depends(use_eatings_manager)],
):
    created_eating = await eatings_manager.create(request, user)
    return created_eating


@router.get("/", response_model=list[EatingResponse])
async def all_eatings(
    user: Annotated[DbUser, Depends(auth_required)],
    eatings_manager: Annotated[EatingsManager, Depends(use_eatings_manager)],
):
    all_eatings = await eatings_manager.all(user)
    return all_eatings


@router.get("/statstic/", response_model=list[DateStatistic])
async def eatings_statistic(
    user: Annotated[DbUser, Depends(auth_required)],
    eatings_manager: Annotated[EatingsManager, Depends(use_eatings_manager)],
    start_month: Annotated[str | None, Query(regex=r"\d{4}-\d{2}")] = None,
    end_month: Annotated[str | None, Query(regex=r"\d{4}-\d{2}")] = None,
):
    if not start_month:
        start_month = date.today().isoformat()[:-3]
    if not end_month:
        end_month = (date.today() + relativedelta(months=1)).isoformat()[:-3]

    statistics = await eatings_manager.get_statistics(user, start_month, end_month)
    return statistics
