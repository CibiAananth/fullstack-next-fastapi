from typing import Optional, Tuple

from app.schemas.extras.current_user import CurrentUser
from jose import JWTError, jwt
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    BaseUser,
    UnauthenticatedUser,
)
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from core.config import config


class CustomUser(BaseUser):
    def __init__(self, user: CurrentUser):
        self.user = user


class AuthBackend(AuthenticationBackend):
    async def authenticate(
        self, request: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, BaseUser]]:
        authorization: Optional[str] = request.headers.get("Authorization")
        if not authorization:
            return AuthCredentials(), UnauthenticatedUser()

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                return AuthCredentials(), UnauthenticatedUser()
        except ValueError:
            return AuthCredentials(), UnauthenticatedUser()

        try:
            payload = jwt.decode(
                token,
                config.SECRET_KEY,
                algorithms=[config.JWT_ALGORITHM],
            )
            user_id: Optional[str] = payload.get("user_id")
        except JWTError:
            return AuthCredentials(), UnauthenticatedUser()

        if user_id is None:
            return AuthCredentials(), UnauthenticatedUser()

        current_user = CurrentUser(id=user_id)
        custom_user = CustomUser(current_user)
        # custom_user.username = current_user.id
        credentials = AuthCredentials(["authenticated"])
        return credentials, custom_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
