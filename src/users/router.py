from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from pydantic import UUID4
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_async_session, get_redis
from src.jinja2.utils import render_to_string
from src.users import schemas, service

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=schemas.UserRetrieve | None)
async def get_user(user_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    return await service.get_user(session, user_id)


@router.get("/", response_model=list[schemas.UserRetrieve])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return await service.get_users(session)


@router.post("/", response_model=schemas.UserRetrieve)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await service.create_user(user.model_dump(), session)


@router.put("/{user_id}", response_model=schemas.UserRetrieve | None)
async def update_user(user_id: UUID4, user: schemas.UserUpdate, session: AsyncSession = Depends(get_async_session)):
    return await service.update_user(user_id, user.model_dump(exclude_unset=True), session)


@router.get("/{user_id}/html", response_class=HTMLResponse)
async def get_user_html(
    request: Request, user_id: UUID4, session: AsyncSession = Depends(get_async_session), redis: Redis = Depends(get_redis)
):
    user = await service.get_user(session, user_id) or {}

    html_name = "users/user_info.html"

    if not (html_page := await redis.get(html_name)):
        html_page = await render_to_string(html_name, {"user": user}, request)
        await redis.set(html_name, html_page, ex=10)

    return html_page
