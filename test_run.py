import asyncio
import time

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.config import settings
from src.domain.user.model.user import UserModel

from src.infrastructure.database.respostiory.user import UserRepo
from src.infrastructure.database.tables.user import User


async def main():
    async def inner(user_email: str) -> UserModel:
        engine = create_async_engine(settings.DATABASE_URL_asyncpg)
        async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
        async with async_session_maker() as session:
            stmt = select(User).where(User.email == 'mrtwon2@example.com')
            result: UserModel = await session.scalar(stmt)
        return result
    result = await inner("mrtwon2@example.com")
    print(result.__dict__)

asyncio.run(main())
time.sleep(10000)
