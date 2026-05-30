from fastapi import HTTPException, status, APIRouter, Depends
from typing import List
from src.db.main import get_session
from src.books.schemas import BookModel, BookCreateModel, PatchBookModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.service import BookService

router = APIRouter()
book_service = BookService()

@router.get('/', response_model=List[BookModel])
async def get_all_books(session: AsyncSession=Depends(get_session)):
    return await book_service.get_all_books(session)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_book(book_data: BookCreateModel, session: AsyncSession=Depends(get_session))-> dict:
    new_book = await book_service.create_book(book_data, session)
    return new_book

@router.get('/{book_uid}', response_model=BookModel)
async def get_book_by_id(book_uid:str, session: AsyncSession=Depends(get_session)) -> dict:
    return await book_service.get_book(session, book_uid)

@router.patch('/{book_uid}', response_model=PatchBookModel)
async def update_book(book_uid:str, book_update_data: PatchBookModel, session: AsyncSession=Depends(get_session))->dict:
    return await book_service.update_book(session, book_uid, book_update_data)
           

@router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    deleted = await book_service.delete_book(session, book_uid)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return None
    
