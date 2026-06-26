from typing import List, TYPE_CHECKING
from sqlmodel import Column, Field, Relationship, SQLModel, false
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

if TYPE_CHECKING:
    from src.books.model import BookModel

class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username: str
    email: str = Field(nullable=False, index=True)
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(
        pg.VARCHAR, nullable=False, server_default="user"
    ))
    is_verified: bool = Field(default=False)
    password_has: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))
    books: List['BookModel'] = Relationship(back_populates='user',sa_relationship_kwargs={'lazy':"selectin"})
    
    def __repr__(self):
        return f"User(uid={self.uid}, username={self.username}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}, is_verified={self.is_verified}, created_at={self.created_at}, updated_at={self.updated_at})"