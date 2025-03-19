from typing import Protocol
from uuid import UUID

from src.domain.user.model.user import UserModel


class IUserRepo(Protocol):
    async def add(self, user: UserModel) -> UserModel:
        raise NotImplementedError

    async def update(self, user: UserModel) -> UserModel:
        raise NotImplementedError

    async def get(self, user_id: UUID | None = None, user_email: str | None = None) -> UserModel | None:
        raise NotImplementedError

    async def get_all(self, ref_code: str | None = None, order_by_date: bool = True) -> list[UserModel]:
        raise NotImplementedError
