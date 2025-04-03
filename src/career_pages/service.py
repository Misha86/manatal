from typing import TYPE_CHECKING, Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.career_pages.models import CareerPage, CareerPageUser

if TYPE_CHECKING:
    from pydantic import UUID4
    from sqlalchemy.engine import Result


async def get_user_career_pages(
    user_id: "UUID4",
    session: AsyncSession,
    skip: int | None = None,
    limit: int | None = None,
) -> CareerPage | None:
    stmt = select(CareerPage).where(CareerPage.users.any(user_id=user_id)).offset(skip).limit(limit)
    result: "Result" = await session.scalars(stmt)
    return result.all()


async def get_user_career_page(career_page_id: "UUID4", user_id: "UUID4", session: AsyncSession) -> CareerPage | None:
    stmt = select(CareerPage).where(CareerPage.id == career_page_id, CareerPage.users.any(user_id=user_id))
    result: "Result" = await session.scalars(stmt)
    return result.one_or_none()


async def update_user_career_page(
    career_page_id: "UUID4", user_id: "UUID4", data: dict[str, Any], session: AsyncSession
) -> CareerPage | None:
    stmt = update(CareerPage).where(CareerPage.id == career_page_id, CareerPage.users.any(user_id=user_id)).values(**data)
    await session.execute(stmt)
    await session.commit()

    return await get_user_career_page(career_page_id, user_id, session)


async def create_career_page(data: dict[str, Any], session: AsyncSession) -> CareerPage:
    new_career_page = CareerPage(**data)
    session.add(new_career_page)
    await session.commit()
    await session.refresh(new_career_page)
    return new_career_page


async def create_career_page_user(data: dict[str, Any], session: AsyncSession) -> CareerPageUser:
    new_career_page_user = CareerPageUser(**data)
    session.add(new_career_page_user)
    await session.commit()
    await session.refresh(new_career_page_user)
    return new_career_page_user
