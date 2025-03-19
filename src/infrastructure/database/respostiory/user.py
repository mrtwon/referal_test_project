from uuid import UUID

from sqlalchemy import select

from src.domain.user.model.user import UserModel
from src.domain.user.repository.repo import IUserRepo
from src.infrastructure.database.respostiory._repo import SQLAlchemyRepo


class UserRepo(IUserRepo, SQLAlchemyRepo):
    async def add(self, user: UserModel) -> UserModel:
        self.session.add(user)
        return user

    async def update(self, user: UserModel) -> UserModel:
        await self.session.merge(user)
        await self.session.flush()
        return user

    async def get(self, user_id: UUID | None = None, user_email: str | None = None) -> UserModel | None:
        if user_id:
            stmt = select(UserModel).where(UserModel.id == user_id)
        elif user_email:
            stmt = select(UserModel).where(UserModel.email == user_email)
        else:
            raise Exception("not enter field for find")
        result = await self.session.scalar(stmt)
        return result

    async def get_all(self, ref_code: str | None = None, order_by_date: bool = True) -> list[UserModel]:
        if order_by_date:
            stmt = (
                select(UserModel).where(UserModel.active_ref_code == ref_code).order_by(UserModel.create_at.desc())
            )
        else:
            stmt = select(UserModel).where(UserModel.active_ref_code == ref_code)
        result = await self.session.scalars(stmt)
        return result.all()
