import json
from datetime import timedelta, datetime
import random
import string
from typing import Literal

from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from .senders import EmailSender
from .schemas import (
    CodeResponse,
    CredentialsResponse,
    CreateUserData,
    DbUser,
    UserUpdateRequest,
)
from .crud import UsersQueries
from .exceptions import VerificationMax, VerificationExpired, IncorrectToken
from ..project.redis import redis_db
from ..project.settings import settings


ACCESS_TOKEN_EXPDELTA = timedelta(days=1)

REFRESH_TOKEN_EXPDELTA = timedelta(days=30)

ALGORITHM = 'HS256'


def generate_code() -> str:
    return ''.join(random.choices(string.digits, k=6))


class TokensSet:

    def _get_exp_delta(
            self, mode: Literal['refresh', 'access']
    ) -> timedelta:
        if mode == 'access':
            return ACCESS_TOKEN_EXPDELTA

        return REFRESH_TOKEN_EXPDELTA

    def create_token(self, user: DbUser,
                     mode: Literal['refresh', 'access']) -> str:
        exp_delta = self._get_exp_delta(mode)
        exp = datetime.utcnow() + exp_delta
        token_sub = {'user_id': user.id, 'email': user.email}
        token_sub_json = json.dumps(token_sub)
        encode_data = {'sub': token_sub_json, 'exp': exp}
        return jwt.encode(encode_data, settings.secret_key, ALGORITHM)

    def decode_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, settings.secret_key,
                                 algorithms=[ALGORITHM])
            assert payload['exp'] > datetime.utcnow().timestamp()
            decoded_sub = json.loads(payload['sub'])
            assert 'user_id' in decoded_sub
            return decoded_sub['user_id']
        except (AssertionError, KeyError, JWTError):
            raise IncorrectToken("Incorrect token")


class AuthManager:

    def __init__(self, session: AsyncSession):
        self._sender = EmailSender()
        self._message = (
            "Your verification code is: {code}"
        )
        self._verification_code_key = 'code:{email}'
        self._verification_code_counter_key = 'code:{email}:counter'
        self._max_validation_count = 5
        self._tokens_set = TokensSet()
        self._users_queries = UsersQueries(session)
        self._redis_session_key = "user:{user_id}:refresh_token"

    async def send_email_code(self, address: str) -> CodeResponse:
        generated_code = generate_code()
        await redis_db.setex(self._verification_code_key.format(email=address), timedelta(minutes=5), generated_code)
        await redis_db.setex(self._verification_code_counter_key.format(email=address), timedelta(minutes=5), 0)
        await self._sender.send_email(address, self._message.format(code=generated_code))
        return CodeResponse(sended=True)

    async def _validate_counts(self, address: str) -> None:
        count = await redis_db.get(self._verification_code_counter_key.format(email=address))
        if count and int(count) >= self._max_validation_count:
            raise VerificationMax("Verification code max attempts")

    async def validate_email_code(self, address: str, code: str) -> bool:
        await self._validate_counts(address)
        right_code = await redis_db.get(self._verification_code_key.format(email=address))
        if not right_code:
            raise VerificationExpired("Verification code has expired")

        await redis_db.incr(self._verification_code_counter_key.format(email=address))
        return code == right_code.decode()

    async def authenticate(self, email: str) -> CredentialsResponse:
        user = await self._users_queries.get_or_none(email=email)
        if not user:
            create_data = CreateUserData(email=email)
            user = await self._users_queries.create(create_data)

        access_token = self._tokens_set.create_token(user, mode='access')
        refresh_token = self._tokens_set.create_token(user, mode='refresh')
        await redis_db.set(self._redis_session_key.format(user_id=user.id), refresh_token)
        return CredentialsResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_from_token(self, token: str) -> DbUser:
        user_id = self._tokens_set.decode_token(token)
        user = await self._users_queries.get_or_none(id=user_id)
        if not user:
            raise IncorrectToken("Incorrect token")

        return DbUser.model_validate(user)

    def refresh_token(self, user: DbUser) -> str:
        return self._tokens_set.create_token(user, 'access')

    async def get_from_refresh_token(self, refresh_token: str) -> DbUser:
        token_user = await self.get_from_token(refresh_token)
        session = await redis_db.get(self._redis_session_key.format(user_id=token_user.id))
        if not session:
            raise IncorrectToken("Incorrect token")

        return token_user

    async def update(self, update_data: UserUpdateRequest, user: DbUser) -> DbUser:
        updated_user = await self._users_queries.update(update_data, user)
        return updated_user

