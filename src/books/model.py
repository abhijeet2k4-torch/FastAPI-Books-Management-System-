from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

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
    create_date: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))
    update_date: datetime = Field(sa_column = Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"BookModel(uid={self.uid}, title={self.title}, author={self.author}, year={self.year})"