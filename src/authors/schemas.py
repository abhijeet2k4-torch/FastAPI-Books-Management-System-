from pydantic import BaseModel

class AuthorModel(BaseModel):
    id:int
    name:str
    email:str

class PatchAuthorModel(BaseModel):
    name:str
    email:str