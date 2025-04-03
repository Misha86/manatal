from fastapi import APIRouter, Depends, Form, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.career_pages import schemas, service
from src.dependencies import get_async_session

router = APIRouter(
    prefix="/career-pages",
    tags=["career_pages"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.CareerPageRetrieve])
async def get_career_pages(
    skip: int | None = None,
    limit: int | None = None,
    session: AsyncSession = Depends(get_async_session),
):
    user_id = "97eea06d-b468-4f6e-9f93-3c9febfb9a9d"
    return await service.get_user_career_pages(user_id, session, skip, limit)


@router.post("/", response_model=schemas.CareerPageRetrieve)
async def create_career_page(career_page: schemas.CareerPageCreate, session: AsyncSession = Depends(get_async_session)):
    user_id = "97eea06d-b468-4f6e-9f93-3c9febfb9a9d"
    career_page = await service.create_career_page(career_page.model_dump(), session)
    params = {"user_id": user_id, "career_page_id": career_page.id}
    await service.create_career_page_user(params, session)
    return career_page


@router.get("/{career_page_id}", response_model=schemas.CareerPageRetrieve | None)
async def get_career_page(career_page_id: UUID4, session: AsyncSession = Depends(get_async_session)):
    user_id = "97eea06d-b468-4f6e-9f93-3c9febfb9a9d"
    if career_page := await service.get_user_career_page(career_page_id, user_id, session):
        return career_page

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{career_page_id}")
async def update_career_page(
    career_page_id: UUID4,
    career_page: schemas.CareerPageUpdate = Form(media_type="multipart/form-data"),
    session: AsyncSession = Depends(get_async_session),
):
    user_id = "97eea06d-b468-4f6e-9f93-3c9febfb9a9d"
    if not (career_page := await service.get_user_career_page(career_page_id, user_id, session)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return career_page
