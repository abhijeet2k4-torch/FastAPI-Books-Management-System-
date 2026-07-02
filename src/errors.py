from typing import Callable

from fastapi.requests import Request
from fastapi.responses import JSONResponse


class BookException(Exception):
    pass

class InvalidTokenError(BookException):
    pass

class RevokedTokenError(BookException):
    pass

class AccessTokenExpiredError(BookException):
    pass

class RefreshTokenExpiredError(BookException):
    pass

class UserAlreadyExistsError(BookException):
    pass

class InsufficientPermissionsError(BookException):
    pass

class BookNotFoundError(BookException):
    pass

class InvalidCredentialsError(BookException):
    pass

def create_exception_handler(status_code: int, initial_detail: str) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: BookException):
        return JSONResponse(content={"detail": initial_detail}, status_code=status_code)

    return exception_handler