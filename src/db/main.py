from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import settings
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    future=True,
    echo=True,
)

async def init_db():
    async with async_engine.begin() as conn:
        from src.books.model import BookModel
        from src.authors.model import AuthorModel
        from src.auth.models import User
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session