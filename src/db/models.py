import uuid
from datetime import datetime
from typing import List, Optional
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Column, Field, Relationship, SQLModel


class BookModel(SQLModel, table=True):
    __tablename__ = 'books'
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    title: str
    author: str
    year: int
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    create_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional['User'] = Relationship(back_populates='books')

    def __repr__(self):
        return f"BookModel(uid={self.uid}, title={self.title}, author={self.author}, year={self.year})"


class AuthorModel(SQLModel, table=True):
    __tablename__ = "authors"
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    name: str
    email: str
    create_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    user: Optional['User'] = Relationship(back_populates='authors')

    def __repr__(self):
        return f"AuthorModel(uid={self.uid}, name={self.name}, email={self.email})"


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
    books: List['BookModel'] = Relationship(back_populates='user', sa_relationship_kwargs={'lazy': "selectin"})
    authors: List['AuthorModel'] = Relationship(back_populates='user', sa_relationship_kwargs={'lazy': "selectin"})
    reviews: List['Review'] = Relationship(back_populates='user', sa_relationship_kwargs={'lazy': "selectin"})
    def __repr__(self):
        return f"User(uid={self.uid}, username={self.username}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}, is_verified={self.is_verified}, created_at={self.created_at}, updated_at={self.updated_at})"

class Review(SQLModel, table=True):
    __tablename__ = 'reviews'
    uid: uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    rating: int = Field(lt=5, gt=0)
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    user: Optional['User'] = Relationship(back_populates='reviews')
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    create_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    update_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    review_text: Optional[str] = Field(default=None)

    def __repr__(self):
        return f"Review(uid={self.uid}, rating={self.rating}, user_uid={self.user_uid}, book_uid={self.book_uid}, create_date={self.create_date}, update_date={self.update_date}, review_text={self.review_text})"
