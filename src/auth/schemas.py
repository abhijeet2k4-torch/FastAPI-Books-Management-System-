from datetime import datetime
import uuid
from typing import List
from pydantic import BaseModel, Field
from src.books.schemas import BookModel

class UserCreateModel(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    username:str = Field(max_length=8)
    email:str = Field(max_length = 40)
    password: str = Field(min_length=6)

class UserModel(BaseModel):
    uid: uuid.UUID 
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool 
    created_at: datetime 
    updated_at: datetime 
    books: List[BookModel]

class UserLoginModel(BaseModel):
    email: str
    password: str