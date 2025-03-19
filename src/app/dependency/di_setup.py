from typing import Protocol

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.domain.base.interface import IUoW
from src.config import settings
from src.infrastructure.database.respostiory.user_referal import UserReferalRepo
from src.infrastructure.database.uow import SQLAlchemyUoW
from src.infrastructure.database.respostiory.user import UserRepo


class Session(Protocol):
    pass


async def get_session() -> AsyncSession:
    async_engine = create_async_engine(
        url=settings.DATABASE_URL_asyncpg
    )

    session = async_sessionmaker(async_engine)
    async with session(expire_on_commit=False) as s:
        yield s


def get_uow(session: Session = Depends()):
    print(type(session))
    print(session)
    return SQLAlchemyUoW(
        session=session,
        users=UserRepo,
        user_referal=UserReferalRepo
    )


def di_setup(app: FastAPI):
    app.dependency_overrides[Session] = get_session
    app.dependency_overrides[IUoW] = get_uow
