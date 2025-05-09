from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException, status

from src.auth.schemas import TokenPayload, User
from src.config import settings


def authenticate_bearer(credentials: str) -> User:
    error_instance = lambda msg: HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=msg, headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            credentials,
            settings.JWT_VERIFYING_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            issuer=settings.JWT_ISSUER,
            options={"require_iat": True, "require_exp": True},
        )
        token_data = TokenPayload(**payload)

    except jwt.PyJWTError:
        raise error_instance("Invalid or expired token")

    except ValueError as err:
        raise error_instance(str(err))

    return token_data.user


def encode_bearer(user_data: dict[str, Any], expires_in_minutes: int, scope: str = None) -> str:

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_in_minutes)

    payload = {
        "token_type": "access",
        "sub": user_data["id"],
        "user": user_data,
        "iat": now,
        "exp": expire,
        "iss": settings.JWT_ISSUER,
    }

    if scope:
        payload["scope"] = scope
    

    token = jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=settings.JWT_ALGORITHM)
    return token



user_data = {
    "id": "0bf588f2-823e-4d3f-a48a-56be3778315c",
    "client_id": 1,
    "full_name": "John Doe",
    "email": "john.doe@example.com",
    "avatar": "https://example.com/avatar.jpg",
}

print(encode_bearer(user_data, 60))
