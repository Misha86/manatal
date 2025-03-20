
from fastapi import APIRouter, Depends, Form, UploadFile
from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}")
async def get_user(user_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    stmt = select(User).where(User.id == user_id)
    result = await session.scalars(stmt)
    return result.one_or_none() or {}


@router.get("/")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.scalars(select(User))
    users = result.all()

    return users


@router.post("/")
async def create_upload_files(logo: UploadFile, name: str = Form(), session: AsyncSession = Depends(get_async_session)):
    new_user = User(name=name, logo=logo)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user
