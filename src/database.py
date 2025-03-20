from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

if TYPE_CHECKING:
    from typing import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> "AsyncGenerator[AsyncSession, None]":
    async with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass
