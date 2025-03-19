from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.base.interface import IUoW
from src.domain.user.repository.repo import IUserRepo
from src.domain.user.repository.uow import IUserUOW
from src.domain.user_referal.repository.repo import IUserReferalRepo
from src.domain.user_referal.repository.uow import IUserReferalUOW


class SQLAlchemyBaseUOW(IUoW):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


class SQLAlchemyUoW(
    SQLAlchemyBaseUOW,
    IUserUOW,
    IUserReferalUOW
):
    users: type[IUserRepo]
    user_referal: type[IUserReferalRepo]

    def __init__(
            self,
            session: AsyncSession,
            users: type[IUserRepo],
            user_referal: type[IUserReferalRepo]
    ):
        self.users = users(session)
        self.user_referal = user_referal(session)
        super().__init__(session)