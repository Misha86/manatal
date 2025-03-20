from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User

if TYPE_CHECKING:
    from fastapi import UploadFile
    from pydantic import UUID4
    from sqlalchemy.engine import Result


async def get_user(session: AsyncSession, user_id: "UUID4") -> User | None:
    stmt = select(User).where(User.id == user_id)
    result: "Result" = await session.scalars(stmt)
    return result.one_or_none()


async def get_users(session: AsyncSession) -> list[User] | None:
    result: "Result" = await session.scalars(select(User))
    return result.all()


async def create_user(logo: "UploadFile", name: str, session: AsyncSession) -> User:
    new_user = User(name=name, logo=logo)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user
