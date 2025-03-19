from datetime import datetime, date
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, and_
from starlette import status

from src.domain.user.model.user import UserModel
from src.domain.user_referal.model.user_referal import UserReferalModel
from src.domain.user_referal.repository.repo import IUserReferalRepo
from src.infrastructure.database.respostiory._repo import SQLAlchemyRepo


class UserReferalRepo(IUserReferalRepo, SQLAlchemyRepo):
    async def add(self, referal: UserReferalModel) -> UserReferalModel:
        self.session.add(referal)
        return referal

    async def update(self, referal: UserReferalModel) -> UserReferalModel:
        await self.session.merge(referal)
        await self.session.flush()
        return referal

    async def get(
            self, email: str | None = None, ref_code: str | None = None, user_id: UUID | None = None,
            end_date: date | None = None, is_delete: bool = False
    ) -> UserReferalModel | None:
        if email:
            stmt = (select(UserReferalModel).join(UserModel, UserModel.id == UserReferalModel.user_id)
                    .where(UserModel.email == email))
        elif ref_code:
            stmt = select(UserReferalModel).where(UserReferalModel.referal_code == ref_code)
        elif user_id:
            stmt = select(UserReferalModel).where(UserReferalModel.user_id == user_id)
        else:
            raise HTTPException(detail='params not found')
        if end_date:
            stmt = stmt.where(UserReferalModel.end_date >= end_date)
        stmt = stmt.where(UserReferalModel.is_delete == is_delete)
        result = await self.session.scalar(stmt)
        return result

    async def get_all(self, user_id: UUID | None = None, email: str | None = None, end_date: date | None = None,
                      is_delete: bool = False) -> list[UserReferalModel]:
        if email:
            stmt = select(UserReferalModel).join(UserModel, UserModel.id == UserReferalModel.user_id)
        elif user_id:
            stmt = select(UserReferalModel).where(UserReferalModel.user_id == user_id)
        else:
            raise HTTPException(detail='params not found')
        if end_date:
            stmt = stmt.where(UserReferalModel.end_date >= end_date)
        if is_delete:
            stmt = stmt.where(UserReferalModel.is_delete == is_delete)
            print(stmt)
        result = await self.session.scalars(stmt)
        return result.all()
