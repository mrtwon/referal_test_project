from datetime import datetime, timezone
from datetime import timedelta
from uuid import UUID

import jwt
from fastapi import APIRouter, HTTPException, Depends
from jose import JWTError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starlette import status
from starlette.requests import Request
from starlette.responses import Response

from src.domain.base.exception import UserNotFoundException
from src.domain.user.model.user import UserModel
from src.domain.user.schema.user import CreateUserSchema, UserAuthSchema, \
    PrivateUserSchema, PublicUserSchema, UpdateUserSchema, UserSchema
from src.app.auth.auth_act import verify_password, get_password_hash, create_access_token
from src.domain.user.service.user import UserServiceABC
from src.domain.user_referal.service.user_referal import UserReferalServiceABC
from src.infrastructure.database.respostiory.user import UserRepo
from src.config import settings
from src.app.auth.dependency import factory_current_user, current_user

user_router = APIRouter(prefix='/users')


@user_router.patch('/', response_model=PrivateUserSchema, status_code=status.HTTP_201_CREATED)
async def update_user_router(
        update_user_schema: UpdateUserSchema,
        user_service: UserServiceABC = Depends(),
        user: UserSchema = Depends(factory_current_user())
):
    return await user_service.update_user(user_id=user.id, update_user_schema=update_user_schema)


@user_router.get('/me', response_model=PrivateUserSchema)
async def current_user_router(user: UserModel = Depends(factory_current_user())):
    return user


@user_router.get('/{user_id}', response_model=PublicUserSchema)
async def get_user_router(
        user_id: UUID,
        user_service: UserServiceABC = Depends()
):
    result = await user_service.get_user(user_id=user_id)
    if result is None:
        raise UserNotFoundException()


# @user_router.get('/current-not-required', response_model=PrivateUserSchema | None)
# async def current_user_router(user: UserModel | None = Depends(factory_current_user(only_auth=False))):
#     return user

# @user_router.get('/current', response_model=PrivateUserSchema)
# async def current_user_router(request: Request):
#     token = request.cookies.get('access_token')
#     if not token:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='token not found')
#     auth_data = settings.get_auth_data()
#     try:
#         payload = jwt.decode(token, auth_data.get('secret_key'), algorithms=auth_data.get('algorithm'))
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='token not valid')
#     except Exception:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     expire = payload.get('exp')
#     expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
#     print(expire_time)
#     print(datetime.now(timezone.utc))
#     if (not expire) or (expire_time < datetime.now(timezone.utc)):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token expired')
#
#     s = await get_session()
#     repo = UserRepo(s)
#     get_user_by_id = await repo.get(user_id=UUID(payload['id']))
#     return get_user_by_id
