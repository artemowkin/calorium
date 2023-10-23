from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import Product
from .services import ProductsManager
from .dependencies import use_products_manager


router = APIRouter()


@router.get('/search/', response_model=list[Product])
async def search_products(products_manager: Annotated[ProductsManager, Depends(use_products_manager)],
                          query: str = '',
                          limit: int = 20) -> list[Product]:
    return await products_manager.search(query, limit)


@router.get('/', response_model=list[Product])
async def all_products(products_manager: Annotated[ProductsManager, Depends(use_products_manager)],
                       ids: str | None = None) -> list[Product]:
    try:
        int_ids = [int(id) for id in ids.split(',')] if ids else None
    except ValueError:
        int_ids = None

    return await products_manager.get_all(int_ids)

