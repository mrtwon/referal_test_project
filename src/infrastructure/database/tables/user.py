import datetime

from sqlalchemy import String, Column, Table, UUID, DATETIME, func, TIMESTAMP, ForeignKey
from src.domain.user.model.user import UserModel
from src.infrastructure.database.tables.base import mapper_registry

user_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID, unique=True, nullable=False, primary_key=True),
    Column("email", String, nullable=False, unique=True),
    Column("password", String, nullable=False),
    Column("active_ref_code", UUID, ForeignKey("user_referal.referal_code"), nullable=True),
    Column("create_at", TIMESTAMP, server_default=func.now(), nullable=False)
)

mapper_registry.map_imperatively(
    UserModel,
    user_table
)
# engine = create_async_engine(settings.DATABASE_URL_asyncpg)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
