from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from src.books.routes import router as book_router
from src.authors.routes import router as author_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router
from .errors import(create_exception_handler,InvalidTokenError, RevokedTokenError, AccessTokenExpiredError, RefreshTokenExpiredError, InsufficientPermissionsError, BookNotFoundError, InvalidCredentialsError, UserAlreadyExistsError)
from .middleware import register_middleware

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting up...")
    await init_db()
    yield
    print("Server is shutting down...")

app = FastAPI(lifespan=lifespan)
version = "0.1.0"


app.add_exception_handler(InvalidTokenError, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={"message": "Invalid token", "resolution": "Please get new token"}))
app.add_exception_handler(RevokedTokenError, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={"message": "Revoked token", "resolution": "Please get new token"}))
app.add_exception_handler(AccessTokenExpiredError, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={"message": "Access token expired", "resolution": "Please get new token"}))
app.add_exception_handler(RefreshTokenExpiredError, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={"message": "Refresh token expired", "resolution": "Please get new token"}))
app.add_exception_handler(InsufficientPermissionsError, create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, initial_detail={"message": "Insufficient permissions", "resolution": "Please contact support"}))
app.add_exception_handler(BookNotFoundError, create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, initial_detail={"message": "Book not found", "resolution": "Please check the book ID"}))
app.add_exception_handler(InvalidCredentialsError, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={"message": "Invalid credentials", "resolution": "Please check your credentials"}))
app.add_exception_handler(UserAlreadyExistsError, create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, initial_detail={"message": "User already exists", "resolution": "Please use a different email"}))

@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Something went wrong", "resolution": "Please try again later"},
    )

register_middleware(app)

app.include_router(book_router, prefix=f"/api/{version}/books",tags=["Books"])
app.include_router(author_router, prefix=f"/api/{version}/authors",tags=["Authors"])
app.include_router(auth_router, prefix=f"/api/{version}/auth",tags=["Authentication"])
