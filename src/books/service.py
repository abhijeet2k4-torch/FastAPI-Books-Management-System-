from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel, PatchBookModel
from sqlmodel import select, desc
from src.db.models import BookModel as BookTable

class BookService:
    async def get_all_books(self,session:AsyncSession):
        statement = select(BookTable).order_by(desc(BookTable.create_date))
        result = await session.exec(statement)
        return result.all()
    
    async def get_user_books(self,user_uid:str,session:AsyncSession):
        statement = select(BookTable).where(BookTable.user_uid == user_uid).order_by(desc(BookTable.create_date))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self,session:AsyncSession,book_uid:str):
        statement = select(BookTable).where(BookTable.uid == book_uid)
        result = await session.exec(statement)
        return result.first()

    async def create_book(self,book_data:BookCreateModel,user_uid:str,session:AsyncSession):
        book_data_dict = book_data.model_dump()
        new_book = BookTable(**book_data_dict)
        new_book.user_uid = user_uid
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self,session:AsyncSession,book_uid:str,update_data:PatchBookModel):
        book_to_update = await self.get_book(session, book_uid)
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for k,v in update_data_dict.items():
            setattr(book_to_update,k,v)
        await session.commit()
        return book_to_update

    async def delete_book(self,session:AsyncSession,book_uid:str):
        book_to_delete = await self.get_book(session, book_uid)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return True
        return None