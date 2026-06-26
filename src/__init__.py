from fastapi import FastAPI
from src.books.routes import router as book_router
from src.authors.routes import router as author_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting up...")
    await init_db()
    yield
    print("Server is shutting down...")

version = "0.1.0"

app = FastAPI(version=version, title="Book_and_author_API", description="A simple API to manage books and authors")

app.include_router(book_router, prefix=f"/api/{version}/books",tags=["Books"])
app.include_router(author_router, prefix=f"/api/{version}/authors",tags=["Authors"])
app.include_router(auth_router, prefix=f"/api/{version}/auth",tags=["Authentication"])
