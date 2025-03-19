from abc import ABC
from uuid import UUID

from src.domain.user.schema.user import GetActiveCode
from src.domain.user_referal.schema.user_referal import CreateReferalSchema, UserReferalSchema, UpdateReferalSchema


class UserReferalServiceABC(ABC):
    async def add_user_referal(self, user_id: UUID, schema: CreateReferalSchema) -> UserReferalSchema:
        ...

    async def update_user_referal(self, user_id: UUID, ref_code: str, schema: UpdateReferalSchema) -> UserReferalSchema:
        ...

    async def get_all_refs(self, user_id: UUID) -> list[UserReferalSchema] | None:
        ...

    async def get_active_ref(self, user_id: UUID, schema: GetActiveCode) -> UserReferalSchema | None:
        ...
