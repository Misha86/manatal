from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr


class User(BaseModel):
    full_name: str
    email: EmailStr
    external_id: int
    avatar_url: str


class UserCreate(User):
    pass


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None


class UserRetrieve(User):
    id: UUID4
    created_at: datetime
    updated_at: datetime
