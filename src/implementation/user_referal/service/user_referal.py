import datetime
from uuid import UUID

from fastapi import HTTPException
from starlette import status

from src.domain.base.exception import AlreadyHasRefCodeException, ForbiddenException, LongTimeLifeRefException
from src.domain.user.schema.user import GetActiveCode
from src.domain.user_referal.model.user_referal import UserReferalModel
from src.domain.user_referal.repository.uow import IUserReferalUOW
from src.domain.user_referal.schema.user_referal import CreateReferalSchema, UserReferalSchema, UpdateReferalSchema
from src.domain.user_referal.service.user_referal import UserReferalServiceABC


class UserReferalService(UserReferalServiceABC):
    def __init__(self, user_referal_uow: IUserReferalUOW):
        self.user_referal_uow = user_referal_uow

    async def add_user_referal(self, user_id: UUID, schema: CreateReferalSchema) -> UserReferalSchema:
        current_date = datetime.date.today()
        result_check_by_active_end_date = await self.user_referal_uow.user_referal.get(user_id=user_id,
                                                                                       end_date=current_date)
        if result_check_by_active_end_date is not None:
            raise AlreadyHasRefCodeException()

        new_user_referal = UserReferalModel(
            referal_code=schema.referal_code,
            end_date=schema.end_date,
            user_id=user_id
        )
        result_check_by_exist_ref_code = await self.user_referal_uow.user_referal.get(ref_code=schema.referal_code)
        if result_check_by_exist_ref_code is not None:
            raise AlreadyHasRefCodeException()

        result = await self.user_referal_uow.user_referal.add(new_user_referal)
        await self.user_referal_uow.commit()
        return UserReferalSchema.model_validate(result)

    async def update_user_referal(self, user_id: UUID,ref_code: str, schema: UpdateReferalSchema) -> UserReferalSchema:
        get_user_referal_by_id = await self.user_referal_uow.user_referal.get(ref_code=ref_code)
        if not get_user_referal_by_id:
            raise AlreadyHasRefCodeException()
        if get_user_referal_by_id.user_id != user_id:
            raise ForbiddenException()
        if schema.end_date >= (datetime.date.today() + datetime.timedelta(days=365 * 2)):
            raise LongTimeLifeRefException()
        get_user_referal_by_id.end_date = schema.end_date
        if not get_user_referal_by_id.is_delete:
            get_user_referal_by_id.is_delete = schema.is_delete
        result = await self.user_referal_uow.user_referal.update(get_user_referal_by_id)
        await self.user_referal_uow.commit()
        return UserReferalSchema.model_validate(result)

    async def get_active_ref(self, user_id: UUID, schema: GetActiveCode) -> UserReferalSchema | None:
        result_ref_by_email = await self.user_referal_uow.user_referal.get(
            email=schema.email,
            user_id=schema.user_id,
            end_date=datetime.date.today(),
            is_delete=False
        )
        if result_ref_by_email is None:
            return None
        return UserReferalSchema.model_validate(result_ref_by_email)

    async def get_all_refs(self, user_id: UUID) -> list[UserReferalSchema] | None:
        result_ref_by_email = await self.user_referal_uow.user_referal.get_all(user_id=user_id)
        return [UserReferalSchema.model_validate(one) for one in result_ref_by_email]