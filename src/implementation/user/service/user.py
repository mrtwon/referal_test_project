import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette import status

from src.domain.base.exception import UserReferenceNotFoundException, UserNotFoundException, \
    AlreadyHasActiveCodeException
from src.domain.user.model.user import UserModel
from src.domain.user.repository.uow import IUserUOW
from src.domain.user.schema.user import CreateUserSchema, PrivateUserSchema, UpdateUserSchema, UserSchema, GetSelfRef
from src.domain.user.service.user import UserServiceABC
from src.app.auth.auth_act import get_password_hash
from src.domain.user_referal.repository.uow import IUserReferalUOW


class UserService(UserServiceABC):
    def __init__(self, user_uow: IUserUOW, user_referal_uow: IUserReferalUOW):
        self.user_uow = user_uow
        self.user_referal_uow = user_referal_uow

    async def add_user(self, add_user_schema: CreateUserSchema) -> UserSchema:
        if add_user_schema.active_ref_code:
            get_ref_by_code = await self.user_referal_uow.user_referal.get(add_user_schema.active_ref_code)
            if not get_ref_by_code:
                raise UserReferenceNotFoundException()
            new_user = UserModel(
                email=add_user_schema.email,
                password=add_user_schema.password,
                active_ref_code=get_ref_by_code.id
            )
            result = await self.user_uow.users.add(new_user)
            return UserSchema.model_validate(result)
        else:
            result = await self.user_uow.users.add(**add_user_schema.dict())
            await self.user_uow.commit()
            return UserSchema.model_validate(result)

    async def update_user(self, user_id: UUID, update_user_schema: UpdateUserSchema) -> UserSchema:
        change_email = update_user_schema.email
        change_password = update_user_schema.password
        new_ref_code = update_user_schema.user_active_ref_code
        
        get_user_by_id = await self.user_uow.users.get(user_id=user_id)
        if not get_user_by_id:
            raise UserNotFoundException()

        if change_password:
            get_user_by_id.password = get_password_hash(change_password)
        if change_email:
            get_user_by_id.email = change_email
        if new_ref_code and get_user_by_id.active_ref_code is None:
            get_ref_by_code = await self.user_referal_uow.user_referal.get(new_ref_code)
            if get_ref_by_code is None:
                raise UserReferenceNotFoundException()
            get_user_by_id.active_ref_code = new_ref_code
        else:
            raise AlreadyHasActiveCodeException()

        await self.user_uow.users.update(get_user_by_id)
        await self.user_uow.commit()

        return UserSchema.model_validate(get_user_by_id)

    async def get_user(self, email: str | None = None, user_id: UUID | None = None) -> UserSchema | None:
        result_get_by_id = await self.user_uow.users.get(user_email=email, user_id=user_id)
        if not result_get_by_id:
            return None
        return UserSchema.model_validate(result_get_by_id)

    async def get_active_referal_by_user_id(self, user_id: UUID, schema: GetSelfRef) -> list[UserSchema]:
        result_get_by_id = await self.user_referal_uow.user_referal.get(user_id=user_id, end_date=datetime.date.today(), is_delete=False)
        if result_get_by_id is None:
            raise UserReferenceNotFoundException()
        result_get_by_ref_code = await self.user_uow.users.get_all(ref_code=result_get_by_id.referal_code, order_by_date=schema.order_by_create_account)
        return [UserSchema.model_validate(one) for one in result_get_by_ref_code]
