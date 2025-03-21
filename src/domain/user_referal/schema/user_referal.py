import datetime
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from src.domain.base.schema import BaseSchema


class UserReferalSchema(BaseSchema):
    referal_code: str
    user_id: UUID
    create_at: datetime.date
    end_date: datetime.date
    is_delete: bool


class UpdateReferalSchema(BaseSchema):
    end_date: Optional[datetime.date] = None
    is_delete: Optional[bool] = None


class SearchByEmailSchema(BaseSchema):
    email: EmailStr


class CreateReferalSchema(BaseSchema):
    referal_code: str
    end_date: datetime.date
