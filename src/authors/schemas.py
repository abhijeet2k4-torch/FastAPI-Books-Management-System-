from datetime import datetime
from pydantic import BaseModel
import uuid

class AuthorModel(BaseModel):
    uid: uuid.UUID
    name: str
    email: str
    create_date: datetime
    update_date: datetime

class AuthorCreateModel(BaseModel):
    name: str
    email: str

class PatchAuthorModel(BaseModel):
    name:str
    email:str