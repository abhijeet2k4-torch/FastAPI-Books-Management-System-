import uuid
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects import postgresql as pg
from datetime import datetime

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

    def __repr__(self):
        return f"AuthorModel(uid={self.uid}, id={self.id}, name={self.name}, email={self.email})"