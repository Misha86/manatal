from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr


class User(BaseModel):
    full_name: str
    email: EmailStr
    external_id: UUID4


class UserCreate(User):
    pass


class UserRetrieve(User):
    id: UUID4
    created_at: datetime
    updated_at: datetime
