from __future__ import annotations

from pathlib import Path
from typing import IO, TYPE_CHECKING, Literal
from urllib.parse import urljoin
from uuid import uuid4

if TYPE_CHECKING:
    from _typeshed import OpenBinaryModeWriting

from .schemas import SavedFile, SavingFile
from .utils import get_extension_by_filename, read_chunked

ALLOWED_STATIC_DIRECTORIES = Literal["products_images"]


class FilesService:

    def __init__(self, static_url: str, static_dir: Path):
        self._static_dir = static_dir
        self._static_url = static_url

    def _generate_system_filename(self, filename: str) -> str:
        file_extension = get_extension_by_filename(filename)
        file_uuid = str(uuid4())
        return f"{file_uuid}{file_extension}"

    def _get_or_create_directory(self, directory: str) -> Path:
        directory_path = self._static_dir / directory
        directory_path.mkdir(exist_ok=True)
        return directory_path

    def _write_file(
        self,
        file_object: IO,
        file_path: Path,
        write_mode: OpenBinaryModeWriting,
        chunk_size: int = 500,
    ):
        with open(file_path, write_mode) as f:
            for chunk in read_chunked(file_object, chunk_size):
                f.write(chunk)

        file_object.seek(0)

    def _generate_url_for_filename(self, directory: ALLOWED_STATIC_DIRECTORIES, filename: str) -> str:
        return urljoin(urljoin(self._static_url, f"{directory}/"), filename)

    def save_file(
        self,
        saving_file: SavingFile,
        directory: ALLOWED_STATIC_DIRECTORIES,
        write_mode: OpenBinaryModeWriting,
        writing_chunk_size: int = 500,
    ) -> SavedFile:
        system_filename = self._generate_system_filename(saving_file.filename)
        directory_path = self._get_or_create_directory(directory)
        file_path = directory_path / system_filename
        self._write_file(saving_file.file_object, file_path, write_mode, writing_chunk_size)
        file_url = self._generate_url_for_filename(directory, system_filename)
        return SavedFile(file_object=saving_file.file_object, filename=saving_file.filename, file_url=file_url)
