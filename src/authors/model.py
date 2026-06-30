import uuid
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy.dialects import postgresql as pg
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import User

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
    name:str
    email:str
    create_date: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    update_date: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    user: Optional['User'] = Relationship(back_populates='authors')

    def __repr__(self):
        return f"AuthorModel(uid={self.uid}, id={self.id}, name={self.name}, email={self.email})"