from typing import TYPE_CHECKING, Callable

from fastapi import Query
from redis.asyncio import from_url

from src.config import settings
from src.database import SessionLocal

if TYPE_CHECKING:
    from typing import AsyncGenerator

    from redis.asyncio import Redis
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_async_session() -> "AsyncGenerator[AsyncSession, None]":
    async with SessionLocal() as session:
        yield session


async def get_redis() -> "AsyncGenerator[Redis, None]":
    session = from_url(url=settings.REDIS_CACHE_URL, encoding="utf-8", decode_responses=False, protocol=3)
    try:
        yield session
    finally:
        await session.aclose()


def get_sort_param(allowed_fields: list[str], default: str) -> Callable[..., str]:
    allowed_fields += [f"-{f}" for f in allowed_fields]

    def process_param(sort: str = Query(default, enum=allowed_fields)) -> str:
        if sort not in allowed_fields:
            sort = default

        direction = "desc" if sort.startswith("-") else "asc"
        field = sort.lstrip("-")
        return f"{field} {direction}"

    return process_param
