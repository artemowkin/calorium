from pathlib import Path
from typing import IO, Generator


def get_extension_by_filename(filename: str) -> str:
    return Path(filename).suffix


def read_chunked(file_object: IO, chunk_size: int = 500) -> Generator[bytes, None, None]:
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break

        yield data
