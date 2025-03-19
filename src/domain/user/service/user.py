from abc import ABC
from uuid import UUID

from src.domain.user.schema.user import CreateUserSchema, UpdateUserSchema, PrivateUserSchema, UserSchema


class UserServiceABC(ABC):
    async def add_user(self, add_user_schema: CreateUserSchema) -> UserSchema:
        ...

    async def update_user(self, user_id: UUID, update_user_schema: UpdateUserSchema) -> UserSchema:
        ...

    async def get_user(self, email: str | None = None, user_id: UUID | None = None) -> UserSchema | None:
        ...

