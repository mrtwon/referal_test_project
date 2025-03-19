from typing import Any

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepo:
    def __init__(self, session: AsyncSession) -> Any:
        self.session = session

    @staticmethod
    def _apply_pagination_to_statement(
        stmt: Select, offset: int = 0, limit: int | None = None
    ) -> Select:
        if limit:
            stmt = stmt.limit(limit)
        return stmt.offset(offset)
