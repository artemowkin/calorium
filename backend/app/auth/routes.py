from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from .schemas import (
    CodeResponse,
    SendEmailCodeRequest,
    CredentialsResponse,
    UserUpdateRequest,
    ValidateCodeRequest,
    UserResponse,
    DbUser,
)
from .dependencies import use_auth_manager, auth_required, use_refresh_token, use_token
from .services import AuthManager
from .exceptions import MessageNotSended, VerificationMax, VerificationExpired


router = APIRouter()


@router.post('/send_code', status_code=201, response_model=CodeResponse)
async def send_code(request: SendEmailCodeRequest,
                    auth_manager: Annotated[AuthManager, Depends(use_auth_manager)]):
    exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message not sended")
    try:
        if await auth_manager.send_email_code(request.email):
            return CodeResponse(sended=True)

        raise exception
    except MessageNotSended:
        raise exception


@router.post('/validate_code', response_model=CredentialsResponse)
async def validate_code(request: ValidateCodeRequest,
                        auth_manager: Annotated[AuthManager, Depends(use_auth_manager)]):
    try:
        is_valid = await auth_manager.validate_email_code(request.email, request.code)
        if is_valid:
            return await auth_manager.authenticate(request.email)
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect code")
    except VerificationMax:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification max attempts")
    except VerificationExpired:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification code expired")


@router.get('/me', response_model=UserResponse)
async def me(user: Annotated[DbUser, Depends(auth_required)]):
    return UserResponse(**user.model_dump())


@router.put('/me', response_model=UserResponse)
async def update_me(request: UserUpdateRequest,
                    auth_manager: Annotated[AuthManager, Depends(use_auth_manager)],
                    user: Annotated[DbUser, Depends(auth_required)]):
    updated_user = await auth_manager.update(request, user)
    return updated_user

@router.post('/refresh', response_model=CredentialsResponse)
async def refresh(token: Annotated[str, Depends(use_token)],
                  auth_manager: Annotated[AuthManager, Depends(use_auth_manager)],
                  db_user: Annotated[DbUser, Depends(use_refresh_token)]):
    access_token = auth_manager.refresh_token(db_user)
    return CredentialsResponse(
        access_token=access_token,
        refresh_token=token
    )

