import uuid
from datetime import datetime
from uuid import UUID

from attrs import field
from pydantic import Field

from src.domain.base.model import entity


@entity
class UserModel:
    id: UUID = field(default=uuid.uuid4())
    email: str
    password: str
    active_ref_code: str
    create_at: datetime | None = None
