from http import HTTPStatus

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions.base import CustomException


class AuthenticationRequiredException(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    error_code = HTTPStatus.UNAUTHORIZED
    message = "Authentication required"


class AuthenticationRequired:
    def __init__(
        self,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ):
        if not token:
            raise AuthenticationRequiredException()
