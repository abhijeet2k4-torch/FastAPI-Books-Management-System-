from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import desc, select
from .model import AuthorModel as AuthorTable
from .schemas import AuthorCreateModel, PatchAuthorModel


class Authorservice:
    async def get_author(self, session: AsyncSession, author_uid: str):
        statement = select(AuthorTable).where(AuthorTable.uid == author_uid)
        result = await session.exec(statement)
        return result.first()

    async def get_author_by_id(self,session:AsyncSession,author_uid:str):
        return await self.get_author(session, author_uid)

    async def get_all_authors(self, session:AsyncSession):
        statement = select(AuthorTable).order_by(desc(AuthorTable.create_date))
        result = await session.exec(statement)
        return result.all()

    async def create_author(self, session:AsyncSession, author_data: AuthorCreateModel):
        author_data_dict = author_data.model_dump()
        new_author = AuthorTable(**author_data_dict)
        session.add(new_author)
        await session.commit()
        await session.refresh(new_author)
        return new_author
    
    async def update_author(self, session:AsyncSession, author_uid:str, update_data: PatchAuthorModel):
        author_to_update = await self.get_author(session, author_uid)
        if not author_to_update:
            return None
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for k,v in update_data_dict.items():
            setattr(author_to_update,k,v)
        await session.commit()
        await session.refresh(author_to_update)
        return author_to_update

    async def delete_author(self, session:AsyncSession, author_uid:str):
        author_to_delete = await self.get_author(session, author_uid)
        if not author_to_delete:
            return None
        await session.delete(author_to_delete)
        await session.commit()
        await session.refresh(author_to_delete)
        return True
