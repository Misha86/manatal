import jwt
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> User:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            user: User = authenticate_bearer(credentials.credentials)
            request.state.user = user
            return user
        
        raise HTTPException(status_code=403, detail="Invalid authorization code.")
