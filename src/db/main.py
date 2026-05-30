from sqlmodel import create_engine, SQLModel, text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from src.config import settings
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

async_engine = AsyncEngine(
    create_engine(
        url=settings.DATABASE_URL,     
        future=True
    )
)

async def init_db():
    async with async_engine.begin() as conn:
        from src.books.model import BookModel
        from src.authors.model import AuthorModel
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session