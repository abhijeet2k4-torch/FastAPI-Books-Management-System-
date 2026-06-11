from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from .utils import create_access_token, decode_token, verify_password
from datetime import timedelta
from src.auth.dependencies import AccessTokenBearer
from .dependencies import RefreshTokenBearer
import datetime
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()

REFRESH_TOKEN_EXPIRY = timedelta(days=7)

@auth_router.post("/signup",response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_Account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    new_user = await user_service.create_user(user_data, session)
    return new_user

@auth_router.post("/login")
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    password_valid = verify_password(password, user.password_has)
    if not password_valid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    token = create_access_token(user_data={"uid": str(user.uid), "email": user.email})
    refresh_token = create_access_token(user_data={"uid": str(user.uid), "email": user.email}, expiry=REFRESH_TOKEN_EXPIRY, refresh=True)

    return JSONResponse(
        content={
            "access_token": token,
            "refresh_token": refresh_token,
            "message": "Login successful",
            "user": {
                "uid": str(user.uid),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }
    )

@auth_router.get("/refresh_token")
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_date = token_details['exp']
    if datetime.datetime.fromtimestamp(expiry_date) > datetime.datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        return JSONResponse(content={
            "access_token": new_access_token
        })
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired refresh token")
    
@auth_router.get('/logout')
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message":"Logged out Successfully"
        },
        status_code=status.HTTP_200_OK
    )