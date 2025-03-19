import datetime
from uuid import UUID
from datetime import date

from attrs import field

from src.domain.base.model import entity


@entity
class UserReferalModel:
    referal_code: str
    user_id: UUID
    create_at: date = field(default=datetime.date.today())
    end_date: date
    is_delete: bool = False
