from fastapi import Depends, HTTPException, status, APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.authors.schemas import AuthorModel, PatchAuthorModel, AuthorCreateModel
from src.authors.services import Authorservice
from src.db import get_session
from src.auth.dependencies import AccessTokenBearer

router = APIRouter()
Authorservice = Authorservice()
access_token_bearer = AccessTokenBearer()

@router.get('/', response_model=List[AuthorModel], status_code=status.HTTP_200_OK)
async def get_all_authors(session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    return await Authorservice.get_all_authors(session)

@router.get('/{author_uid}', response_model=AuthorModel, status_code=status.HTTP_200_OK)
async def get_author_by_id(author_uid:str, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    author = await Authorservice.get_author_by_id(session, author_uid)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author

@router.post("/", response_model=AuthorModel, status_code=status.HTTP_201_CREATED)
async def create_author(author_data: AuthorCreateModel, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    return await Authorservice.create_author(session, author_data)

@router.patch('/{author_uid}', response_model=AuthorModel, status_code=status.HTTP_200_OK)
async def update_author(author_uid:str, update_data: PatchAuthorModel, session:AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    author = await Authorservice.update_author(session, author_uid, update_data)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author

@router.delete('/{author_uid}', response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(author_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    deleted = await Authorservice.delete_author(session, author_uid)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return None

