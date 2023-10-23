from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, ColumnElement

from .schemas import CreateUserData, DbUser, UserUpdateRequest
from .models import User


class UsersQueries:

    def __init__(self, session: AsyncSession):
        self._session = session

    def _get_where(self, id: int | None = None, email: str | None = None) -> ColumnElement[bool]:
        if id:
            return User.id == id
        else:
            return User.email == email

    async def get_or_none(self, id: int | None = None, email: str | None = None) -> DbUser | None:
        assert any((id, email)), "At least one of id or email must be seted"
        where = self._get_where(id, email)
        stmt = select(User).where(where)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return DbUser.model_validate(user) if user else None

    async def create(self, data: CreateUserData) -> DbUser:
        stmt = insert(User).returning(User).values(**data.model_dump())
        result = await self._session.execute(stmt)
        user = result.scalar_one()
        return DbUser.model_validate(user)

    async def update(self, data: UserUpdateRequest, user: DbUser) -> DbUser:
        stmt = update(User).returning(User).values(
            **data.model_dump(exclude_none=True, exclude_unset=True),
        ).where(User.id == user.id)
        result = await self._session.execute(stmt)
        updated_user = result.scalar_one()
        return DbUser.model_validate(updated_user)

