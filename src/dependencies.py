from typing import TYPE_CHECKING

from src.core.database import SessionLocal

if TYPE_CHECKING:
    from typing import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> "AsyncGenerator[AsyncSession, None]":
    async with SessionLocal() as session:
        yield session
