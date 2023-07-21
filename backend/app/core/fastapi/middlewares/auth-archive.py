from typing import Optional, Tuple

from jose import JWTError, jwt
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config import config


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, SimpleUser]]:
        authorization: Optional[str] = conn.headers.get("Authorization")
        if not authorization:
            return None

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return None
        except ValueError:
            return None

        if not token:
            return None

        try:
            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            user_id: Optional[str] = payload.get("user_id")
            if user_id is None:
                return None
        except JWTError:
            raise AuthenticationError("Invalid token")

        user = SimpleUser(user_id)
        credentials = AuthCredentials(["authenticated"])
        return credentials, user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
