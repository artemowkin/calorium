from typing import Annotated

from app.auth.dependencies import auth_not_required, auth_required
from app.auth.schemas import DbUser
from app.files.schemas import SavingFile
from app.utils.schemas import PaginatedResponse
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status

from .dependencies import use_create_product_handler, use_products_manager
from .handlers import CreateProductHandler
from .schemas import CreateProductModel, Product
from .services import ProductsManager

router = APIRouter()


@router.get("/search/", response_model=list[Product])
async def search_products(
    products_manager: Annotated[ProductsManager, Depends(use_products_manager)], query: str = "", limit: int = 20
) -> list[Product]:
    return await products_manager.search(query, limit)


@router.get("/", response_model=PaginatedResponse[Product])
async def all_products(
    products_manager: Annotated[ProductsManager, Depends(use_products_manager)],
    user: Annotated[DbUser | None, Depends(auth_not_required)],
    page: int = 1,
    per_page: int = 50,
    ids: str | None = None,
    my: bool = False,
) -> PaginatedResponse[Product]:
    try:
        int_ids = [int(id) for id in ids.split(",")] if ids else None
    except ValueError:
        int_ids = None

    return await products_manager.get_all(page, per_page, int_ids, user if my else None)


@router.post("/", response_model=Product)
async def create_product(
    handler: Annotated[CreateProductHandler, Depends(use_create_product_handler)],
    user: Annotated[DbUser, Depends(auth_required)],
    image: UploadFile,
    title: str = Body(),
    kkal: float = Body(),
):
    if not image.filename:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Вы пытаетесь загрузить файл без имени")

    saving_file = SavingFile(file_object=image.file, filename=image.filename)  # pyright: ignore[reportArgumentType]
    create_model = CreateProductModel(title=title, kkal=kkal, owner=user)
    created_product = await handler.execute(saving_file, create_model)
    return created_product
