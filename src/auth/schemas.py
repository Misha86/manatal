from datetime import datetime, timezone

from pydantic import UUID4, BaseModel, field_validator

from src.config import settings


class User(BaseModel):
    id: UUID4
    client_id: UUID4
    full_name: str
    email: str
    avatar: str


class TokenPayload(BaseModel):
    token_type: str
    exp: datetime
    iat: datetime
    user: User
    iss: str
    scope: str | None = None

    @field_validator("token_type", mode="before")
    @classmethod
    def validate_token_type(cls, value: str) -> str:
        if value in ["access"]:
            return value
        raise ValueError("Invalid token type")

    @field_validator("iat", mode="before")
    @classmethod
    def validate_iat(cls, value: datetime) -> datetime:
        utc_timezone = timezone.utc
        iat_datetime = datetime.fromtimestamp(value, tz=utc_timezone)
        
        if datetime.fromtimestamp(value, tz=utc_timezone) > datetime.now(tz=utc_timezone):
            raise ValueError("iat datetime is before the current time")
        return iat_datetime

    @field_validator("scope", mode="before")
    @classmethod
    def validate_scope(cls, scope: str | None) -> str | None:
        if scope and scope in settings.JWT_DISALLOW_SCOPES:
            raise ValueError("Invalid token scope")

        return scope
