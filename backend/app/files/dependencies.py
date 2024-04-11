from app.project.settings import STATIC_ROOT, STATIC_URL

from .services import FilesService


async def use_files_service() -> FilesService:
    return FilesService(STATIC_URL, STATIC_ROOT)
