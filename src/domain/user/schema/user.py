import datetime
from typing import Optional
from uuid import UUID
from pydantic import EmailStr
from src.domain.base.schema import BaseSchema


class UserSchema(BaseSchema):
    id: UUID
    email: str
    active_ref_code: str
    create_at: datetime.datetime
    password: str


class PublicUserSchema(BaseSchema):
    id: UUID
    email: str


class PrivateUserSchema(PublicUserSchema):
    active_ref_code: str
    create_at: datetime.datetime


class CreateUserSchema(BaseSchema):
    email: str
    password: str
    active_ref_code: Optional[str] = None


class GetSelfRef(BaseSchema):
    order_by_create_account: bool


class GetActiveCode(BaseSchema):
    user_id: UUID | None = None
    email: str | None = None


class UpdateUserSchema(BaseSchema):
    user_active_ref_code: str | None = None
    password: str | None = None
    email: EmailStr | None = None


class UserAuthSchema(BaseSchema):
    email: str
    password: str
