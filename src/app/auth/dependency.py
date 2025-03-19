from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from src.domain.base.exception import TokenNotFoundException, TokeNotValidException, UserNotFoundException
from src.domain.user.model.user import UserModel
from src.config import settings
from src.domain.user.schema.user import PrivateUserSchema, UserSchema
from src.domain.user.service.user import UserServiceABC
from src.infrastructure.database.respostiory.user import UserRepo


async def get_session():
    engine = create_async_engine(settings.DATABASE_URL_asyncpg)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    return async_session_maker()


def get_token_from_cookie(request: Request):
    token = request.cookies.get('access_token')
    return token


async def current_user(
        request: Request,
        response: Response,
        token=Depends(get_token_from_cookie),
        user_service: UserServiceABC = Depends()
) -> UserSchema:
    if not token:
        raise TokenNotFoundException()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except JWTError:
        raise TokeNotValidException()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    result_get_user_by_id = await user_service.get_user(user_id=UUID(payload.get('id')))
    if not result_get_user_by_id:
        raise UserNotFoundException()
    return result_get_user_by_id


async def current_user_or_none(
        request: Request,
        response: Response,
        token=Depends(get_token_from_cookie),
        user_service: UserServiceABC = Depends()
) -> UserSchema | None:
    if not token:
        return None
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
    except JWTError:
        return None
    except Exception:
        return None

    result_get_user_by_id = await user_service.get_user(user_id=UUID(payload.get('id')))
    return result_get_user_by_id


def factory_current_user(only_auth: bool = True):
    if only_auth:
        return current_user
    return current_user_or_none
