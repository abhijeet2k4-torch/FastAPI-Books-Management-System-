from fastapi import HTTPException, status, APIRouter, Depends
from typing import List
from src.db.main import get_session
from src.books.schemas import BookModel, BookCreateModel, PatchBookModel
from sqlalchemy.ext.asyncio import AsyncSession
from src.books.service import BookService
from src.auth.dependencies import AccessTokenBearer, RoleChekcer
from src.errors import BookNotFoundError

router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChekcer(['admin',"user"])

@router.get(
    '/',
    response_model=List[BookModel],
    dependencies=[Depends(role_checker)],
    responses={status.HTTP_200_OK: {"description": "Books returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}},
)
async def get_all_books(session: AsyncSession=Depends(get_session), user_details=Depends(access_token_bearer)) -> List[BookModel]:
    return await book_service.get_all_books(session)

@router.get(
    '/user/{user_uid}',
    response_model=List[BookModel],
    dependencies=[Depends(role_checker)],
    responses={status.HTTP_200_OK: {"description": "Books returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}},
)
async def get_user_book_submissions(user_uid:str,session: AsyncSession=Depends(get_session), user_details=Depends(access_token_bearer)) -> List[BookModel]:
    return await book_service.get_user_books(user_uid,session)

@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=BookModel,
    dependencies=[Depends(role_checker)],
    responses={status.HTTP_201_CREATED: {"description": "Book created"}, status.HTTP_400_BAD_REQUEST: {"description": "Invalid request body"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}, status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation error"}},
)
async def create_book(book_data: BookCreateModel, session: AsyncSession=Depends(get_session), token_details: dict=Depends(access_token_bearer), _:bool = Depends(role_checker))-> dict:
    user_id = token_details.get('user')['user_uid']
    new_book = await book_service.create_book(book_data,user_id, session)
    return new_book

@router.get(
    '/{book_uid}',
    response_model=BookModel,
    dependencies=[Depends(role_checker)],
    responses={status.HTTP_200_OK: {"description": "Book returned"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}, status.HTTP_404_NOT_FOUND: {"description": "Book not found"}},
)
async def get_book_by_id(book_uid:str, session: AsyncSession=Depends(get_session), user_details=Depends(access_token_bearer)) -> dict:
    return await book_service.get_book(session, book_uid)

@router.patch(
    '/{book_uid}',
    response_model=PatchBookModel,
    dependencies=[Depends(role_checker)],
    responses={status.HTTP_200_OK: {"description": "Book updated"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}, status.HTTP_404_NOT_FOUND: {"description": "Book not found"}, status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Validation error"}},
)
async def update_book(book_uid:str, book_update_data: PatchBookModel, session: AsyncSession=Depends(get_session), user_details=Depends(access_token_bearer))->dict:
    return await book_service.update_book(session, book_uid, book_update_data)
           

@router.delete(
    '/{book_uid}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(role_checker)],
    responses={status.HTTP_204_NO_CONTENT: {"description": "Book deleted"}, status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized"}, status.HTTP_403_FORBIDDEN: {"description": "Invalid or expired token"}, status.HTTP_404_NOT_FOUND: {"description": "Book not found"}},
)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)):
    deleted = await book_service.delete_book(session, book_uid)
    if not deleted:
        raise BookNotFoundError("Book not found")


    
