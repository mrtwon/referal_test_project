from fastapi import APIRouter, Depends

from src.app.auth.dependency import factory_current_user
from src.domain.base.exception import ActiveRefCodeNotFoundException
from src.domain.user.schema.user import UserSchema, GetActiveCode
from src.domain.user_referal.schema.user_referal import CreateReferalSchema, UpdateReferalSchema, UserReferalSchema
from src.domain.user_referal.service.user_referal import UserReferalServiceABC

referal_router = APIRouter(prefix='/referal')


@referal_router.get('/me/active_ref', response_model=UserReferalSchema)
async def get_active_ref(
        user: UserSchema = Depends(factory_current_user()),
        user_referal_service: UserReferalServiceABC = Depends()
):
    result = await user_referal_service.get_active_ref(user.id, GetActiveCode(user_id=user.id))
    if result is None:
        raise ActiveRefCodeNotFoundException()
    return result


@referal_router.get('/me/refs', response_model=list[UserReferalSchema])
async def get_all_ref(
        user: UserSchema = Depends(factory_current_user()),
        user_referal_service: UserReferalServiceABC = Depends()
):
    return await user_referal_service.get_all_refs(user_id=user.id)


@referal_router.post('/me/refs', response_model=UserReferalSchema)
async def add_ref(
        schema: CreateReferalSchema,
        user: UserSchema = Depends(factory_current_user()),
        user_referal_service: UserReferalServiceABC = Depends()
):
    return await user_referal_service.add_user_referal(user_id=user.id, schema=schema)


@referal_router.patch('/me/refs/{ref_code}', response_model=UserReferalSchema)
async def update_ref(
        ref_code: str,
        schema: UpdateReferalSchema,
        user: UserSchema = Depends(factory_current_user()),
        user_referal_service: UserReferalServiceABC = Depends()
):
    return await user_referal_service.update_user_referal(user_id=user.id, ref_code=ref_code, schema=schema)


@referal_router.get('/email/{email}/active_ref', response_model=UserReferalSchema | None)
async def get_active_ref_for_user(
        email: str,
        user: UserSchema = Depends(factory_current_user()),
        user_referal_service: UserReferalServiceABC = Depends()
):
    result = await user_referal_service.get_active_ref(user.id, GetActiveCode(email=email))
    if result is None:
        raise ActiveRefCodeNotFoundException()
    return result
