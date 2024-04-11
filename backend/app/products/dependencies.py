from typing import Annotated

from app.files.dependencies import use_files_service
from app.files.services import FilesService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..project.dependencies import use_session
from .handlers import CreateProductHandler
from .services import ProductsManager


async def use_products_manager(session: Annotated[AsyncSession, Depends(use_session)]) -> ProductsManager:
    return ProductsManager(session)


async def use_create_product_handler(
    products_service: Annotated[ProductsManager, Depends(use_products_manager)],
    files_service: Annotated[FilesService, Depends(use_files_service)],
) -> CreateProductHandler:
    return CreateProductHandler(products_service, files_service)
