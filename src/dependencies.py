from typing import TYPE_CHECKING

from redis.asyncio import from_url

from src.config import settings
from src.core.database import SessionLocal

if TYPE_CHECKING:
    from typing import AsyncGenerator, AsyncIterator

    from redis.asyncio import Redis
    from sqlalchemy.ext.asyncio import AsyncSession

async def get_async_session() -> "AsyncGenerator[AsyncSession, None]":
    async with SessionLocal() as session:
        yield session


async def get_redis() -> "AsyncIterator[Redis]":
    session = from_url(url=settings.REDIS_CACHE_URL, encoding="utf-8", decode_responses=True)
    try:
        yield session
    finally:
        await session.aclose()
