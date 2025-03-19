import datetime
from uuid import UUID

from src.domain.user_referal.model.user_referal import UserReferalModel


class IUserReferalRepo:
    async def add(self, referal: UserReferalModel) -> UserReferalModel:
        raise NotImplementedError

    async def update(self, referal: UserReferalModel) -> UserReferalModel:
        raise NotImplementedError

    async def get(self, email: str | None = None, ref_code: str | None = None, user_id: UUID | None = None, end_date: datetime.date | None = None, is_delete: bool = False) -> UserReferalModel | None:
        raise NotImplementedError

    async def get_all(self, user_id: UUID | None = None, email: str | None = None, end_date: datetime.date | None = None, is_delete: bool = False) -> list[UserReferalModel]:
        raise NotImplementedError
