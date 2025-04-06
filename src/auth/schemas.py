from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, field_validator
from pytz import UTC

from src.config import settings


class User(BaseModel):
    full_name: str
    email: EmailStr
    external_id: UUID4


class UserCreate(User):
    pass


class UserUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None


class UserRetrieve(User):
    id: UUID4
    created_at: datetime
    updated_at: datetime


class TokenPayload(BaseModel):
    token_type: str
    exp: datetime
    iat: datetime
    user: User
    iss: str
    scope: str | None

    @field_validator("token_type", mode="before")
    @classmethod
    def validate_token_type(cls, value: str) -> str:
        if value in ["access"]:
            return value
        raise ValueError("Invalid token type")

    @field_validator("iat", mode="before")
    @classmethod
    def validate_iat(cls, value: datetime) -> datetime:
        if value > datetime.now(tz=UTC):
            raise ValueError("iat datetime is before the current time")
        return value

    @field_validator("scope", mode="before")
    @classmethod
    def validate_scope(cls, scope: str | None) -> str | None:
        if scope and scope in settings.JWT_DISALLOW_SCOPES:
            raise ValueError("Invalid token scope")

        return scope
