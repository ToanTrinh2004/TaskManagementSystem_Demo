from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings


def create_access_token(user_id: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE
    )
    payload = {
        "sub": user_id,
        "exp": expire,
        "type" : "access"
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def create_refresh_token(user_id : str):
    expire = datetime.now(timezone.utc) + timedelta(
        days = settings.REFRESH_TOKEN_EXPIRE)
    payload = {
        "sub": user_id,
        "exp": expire,
        "type" : "refresh"
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )

