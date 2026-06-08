import uuid
import bcrypt
import jwt
from src.config import settings
from datetime import datetime, timedelta
import logging

ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh
    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    
    return token

def decode_token(token:str) ->str:
    try:
        token_data = jwt.decode(
            jwt = token,
            key = settings.JWT_SECRET_KEY,
            algorithms = [settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        logging.error(f"Error decoding token: {e}")
        return None
    return token_data