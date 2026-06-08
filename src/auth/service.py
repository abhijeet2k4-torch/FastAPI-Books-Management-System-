from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from .schemas import UserCreateModel
from .utils import generate_password_hash

class UserService:
    async def get_user_by_email(self,email:str, session: AsyncSession) -> User:
        result = await session.exec(
            select(User).where(User.email == email)
        )
        user = result.one_or_none()
        return user
    
    async def user_exists(self,email:str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        return True if user else False
    
    async def create_user(self,user_data: UserCreateModel, session: AsyncSession) -> User:
        user_data_dict = user_data.model_dump()
        user_data_dict["password_has"] = generate_password_hash(user_data.password)
        new_user = User(**user_data_dict)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user