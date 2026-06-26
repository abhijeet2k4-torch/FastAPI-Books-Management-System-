from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import User
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
    create_date: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    update_date: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    user: Optional['User'] = Relationship(back_populates='books')

    def __repr__(self):
        return f"BookModel(uid={self.uid}, title={self.title}, author={self.author}, year={self.year})"