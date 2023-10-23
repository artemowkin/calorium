from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.exceptions import IncorrectToken

from app.auth.schemas import DbUser

from .services import AuthManager
from ..project.dependencies import use_session


oauth2_scheme = HTTPBearer(auto_error=True)


def use_auth_manager(session: Annotated[AsyncSession, Depends(use_session)]) -> AuthManager:
    return AuthManager(session)


async def use_token(credentials: Annotated[HTTPAuthorizationCredentials, Security(oauth2_scheme)]) -> str:
    return credentials.credentials


async def auth_required(auth_manager: Annotated[AuthManager, Depends(use_auth_manager)],
                        credentials: Annotated[HTTPAuthorizationCredentials, Security(oauth2_scheme)]) -> DbUser:
    return await auth_manager.get_from_token(credentials.credentials)


async def use_refresh_token(credentials: Annotated[HTTPAuthorizationCredentials, Security(oauth2_scheme)],
                            auth_manager: Annotated[AuthManager, Depends(use_auth_manager)]) -> DbUser:
    try:
        db_user = await auth_manager.get_from_refresh_token(credentials.credentials)
        return db_user
    except IncorrectToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token")

