from sqlmodel import Column, Field, SQLModel, false
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg

class User(SQLModel, table= True):
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
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))  
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False, default=datetime.now))

    def __repr__(self):
        return f"User(uid={self.uid}, username={self.username}, email={self.email}, first_name={self.first_name}, last_name={self.last_name}, is_verified={self.is_verified}, created_at={self.created_at}, updated_at={self.updated_at})"