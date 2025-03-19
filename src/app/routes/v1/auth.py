from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from starlette.responses import Response

from src.app.auth.auth_act import get_password_hash, verify_password, create_access_token
from src.domain.user.schema.user import CreateUserSchema, UserAuthSchema, PrivateUserSchema
from src.domain.user.service.user import UserServiceABC

auth_router = APIRouter(prefix='/auth')


@auth_router.post('/register', response_model=PrivateUserSchema)
async def user_register_router(
        user_create: CreateUserSchema,
        user_service: UserServiceABC = Depends()
):
    get_user_by_email = await user_service.get_user(email=user_create.email)
    if get_user_by_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user already exist')
    hash_password = get_password_hash(user_create.password)
    user_create.password = hash_password
    result_add = await user_service.add_user(user_create)
    return result_add


@auth_router.post('/login')
async def user_auth_router(
        response: Response,
        user_auth: UserAuthSchema,
        user_service: UserServiceABC = Depends()
):
    result_get_user_by_email = await user_service.get_user(email=user_auth.email)
    if result_get_user_by_email and verify_password(user_auth.password, result_get_user_by_email.password):
        exp = (datetime.now() + timedelta(seconds=20)).timestamp()
        new_token = create_access_token(
            {
                'id': result_get_user_by_email.id.__str__(),
                'email': result_get_user_by_email.email,
                'exp': exp
            })
        response.set_cookie('access_token', new_token, httponly=True)
        return {'access_token': new_token}
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='email or password not valid')


@auth_router.get('/logout', status_code=status.HTTP_200_OK)
async def user_logout_router(response: Response):
    response.delete_cookie('access_token')
