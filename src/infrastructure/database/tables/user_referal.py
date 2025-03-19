import datetime

from sqlalchemy import Table, Column, String, UUID, ForeignKey, DATE, Boolean

from src.domain.user_referal.model.user_referal import UserReferalModel
from .base import mapper_registry

user_referal = Table(
    "user_referal",
    mapper_registry.metadata,
    Column("referal_code", String(16), primary_key=True, unique=True),
    Column("user_id", UUID, ForeignKey("users.id"), nullable=False),
    Column("create_at", DATE, nullable=False, default=datetime.datetime.now()),
    Column("end_date", DATE, nullable=False),
    Column("is_delete", Boolean, default=False)
)

mapper_registry.map_imperatively(
    UserReferalModel,
    user_referal
)