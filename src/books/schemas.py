from pydantic import BaseModel
import uuid
from datetime import datetime

class BookModel(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    year: int
    create_date: datetime
    update_date: datetime

class BookCreateModel(BaseModel):
    title: str
    author: str
    year: int

class PatchBookModel(BaseModel):
    title: str
    author: str
    year: int
