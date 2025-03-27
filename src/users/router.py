from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import get_async_session
from src.users import schemas, service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=schemas.UserData)
async def get_user(user_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    return await service.get_user(session, user_id) or {}


@router.get("/", response_model=list[schemas.UserData])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return await service.get_users(session)


@router.post("/", response_model=schemas.UserData)
async def create_upload_files(logo: UploadFile, name: str = Form(), session: AsyncSession = Depends(get_async_session)):
    return await service.create_user(logo, name, session)


@router.get("/{user_id}/html", response_class=HTMLResponse)
async def get_user_html(user_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    user = await service.get_user(session, user_id) or {}

    template = settings.JINJA2_ENV.get_template("users/user_info.html")
    output = await template.render_async({"user": user})

    return output
