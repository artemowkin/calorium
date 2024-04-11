from tempfile import SpooledTemporaryFile
from typing import BinaryIO

from pydantic import BaseModel, ConfigDict


class SavedFile(BaseModel):
    file_object: SpooledTemporaryFile
    file_url: str
    filename: str

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SavingFile(BaseModel):
    file_object: SpooledTemporaryFile
    filename: str

    model_config = ConfigDict(arbitrary_types_allowed=True)
