from typing import TYPE_CHECKING, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.career_pages.models import User

if TYPE_CHECKING:
    from pydantic import UUID4
    from sqlalchemy.engine import Result


async def get_user(session: AsyncSession, user_id: "UUID4") -> User | None:
    stmt = select(User).where(User.id == user_id)
    result: "Result" = await session.scalars(stmt)
    return result.one_or_none()


async def update_user(user_id: "UUID4", data: dict[str, Any], session: AsyncSession) -> User:
    stmt = update(User).where(User.id == user_id).values(**data)
    await session.execute(stmt)
    await session.commit()

    return await get_user(session, user_id)


async def get_users(session: AsyncSession) -> list[User] | None:
    result: "Result" = await session.scalars(select(User))
    return result.all()


async def create_user(data: dict[str, Any], session: AsyncSession) -> User:
    new_user = User(**data)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
