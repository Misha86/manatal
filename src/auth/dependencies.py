from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.schemas import User
from src.auth.utils import authenticate_bearer


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
