from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from src.career_pages import schemas, service
from src.dependencies import get_async_session

router = APIRouter(
    prefix="/career-pages",
    tags=["career_pages"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[schemas.CareerPageRetrieve])
async def get_career_pages(session: AsyncSession = Depends(get_async_session)):
    user_id = "8271f523-780e-4629-b7cf-9f6f75f559a0"

    return await service.get_user_career_pages(user_id, session)


@router.post("/", response_model=schemas.CareerPageRetrieve)
async def create_career_page(career_page: schemas.CareerPageCreate, session: AsyncSession = Depends(get_async_session)):
    user_id = "8271f523-780e-4629-b7cf-9f6f75f559a0"
    career_page = await service.create_career_page(career_page.model_dump(), session)
    params = {"user_id": user_id, "career_page_id": career_page.id, "status": "active", "role": "owner"}
    await service.create_career_page_user(params, session)
    return career_page


@router.get("/{id}", response_model=schemas.CareerPageRetrieve | None)
async def get_career_page(id: UUID4, session: AsyncSession = Depends(get_async_session)):
    user_id = "8271f523-780e-4629-b7cf-9f6f75f559a0"
    return await service.get_user_career_page(id, user_id, session)


@router.put("/{id}", response_model=schemas.CareerPageRetrieve | None)
async def update_career_page(
    id: UUID4, career_page: schemas.CareerPageUpdate, session: AsyncSession = Depends(get_async_session)
):
    user_id = "8271f523-780e-4629-b7cf-9f6f75f559a0"
    # user_id = "e26b057d-4727-4f66-9321-2dbc69f4a5ff"
    return await service.update_user_career_page(id, user_id, career_page.model_dump(exclude_unset=True), session)
