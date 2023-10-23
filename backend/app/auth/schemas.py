from typing import Literal
from pydantic import BaseModel, EmailStr, ConfigDict


class CodeResponse(BaseModel):
    sended: bool


class SendEmailCodeRequest(BaseModel):
    email: EmailStr


class ValidateCodeRequest(BaseModel):
    email: EmailStr
    code: str


class CredentialsResponse(BaseModel):
    access_token: str
    refresh_token: str


class CreateUserData(BaseModel):
    email: str


class BaseUser(BaseModel):
    email: str
    height: int | None = None
    weight: float | None = None
    age: int | None = None
    sex: Literal['male', 'female'] | None = None
    activity: Literal['lowest', 'low', 'middle', 'high', 'highest'] | None = None


class UserUpdateRequest(BaseModel):
    height: int | None = None
    weight: float | None = None
    age: int | None = None
    sex: Literal['male', 'female'] | None = None
    activity: Literal['lowest', 'low', 'middle', 'high', 'highest'] | None = None


class DbUser(BaseUser):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseUser):
    id: int

