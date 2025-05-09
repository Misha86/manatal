from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi_pagination import Page
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import JWTBearer
from src.auth.schemas import User
from src.career_pages import schemas, service
from src.dependencies import get_async_session, get_sort_param

router = APIRouter(
    prefix="/career-pages",
    tags=["career_pages"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("/", response_model=Page[schemas.CareerPageRetrieve])
async def get_career_pages(
    sort: str = Depends(get_sort_param(["name", "created_at", "status"], "name")),
    user: User = Depends(JWTBearer()),
    session: AsyncSession = Depends(get_async_session),
):
    return await service.get_paginated_user_career_pages(user.id, session, sort)


@router.post("/", response_model=schemas.CareerPageRetrieve, status_code=status.HTTP_201_CREATED)
async def create_career_page(
    career_page: schemas.CareerPageCreate,
    user: User = Depends(JWTBearer()),
    session: AsyncSession = Depends(get_async_session),
):
    career_page = await service.create_career_page(career_page.model_dump(), session)
    params = {"user_id": user.id, "career_page_id": career_page.id, "status": "active"}
    await service.create_career_page_user(params, session)
    return career_page


@router.get("/{career_page_id}", response_model=schemas.CareerPageRetrieve | None)
async def get_career_page(career_page_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    user_id = "9a3d5cce-cfed-4334-a829-d8195e3fcb48"
    if career_page := await service.get_user_career_page(career_page_id, user_id, session):
        return career_page

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{career_page_id}")
async def update_career_page(
    career_page_id: UUID4,
    career_page: schemas.CareerPageUpdate = Form(media_type="multipart/form-data"),
    session: AsyncSession = Depends(get_async_session),
):
    user_id = "9a3d5cce-cfed-4334-a829-d8195e3fcb48"
    if not (career_page := await service.get_user_career_page(career_page_id, user_id, session)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    career_page = await service.update_user_career_page(career_page_id, user_id, session)

    return career_page
