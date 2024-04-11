from app.files.schemas import SavingFile
from app.files.services import FilesService

from .schemas import CreateProductModel, Product
from .services import ProductsManager


class CreateProductHandler:

    def __init__(self, products_service: ProductsManager, files_service: FilesService):
        self._products_service = products_service
        self._files_service = files_service

    async def execute(self, saving_file: SavingFile, create_data: CreateProductModel) -> Product:
        saved_file = self._files_service.save_file(saving_file, "products_images", "wb")
        create_data.file_url = saved_file.file_url
        created_product = await self._products_service.create(create_data)
        return created_product
