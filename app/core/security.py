from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token() -> str:
    expire = datetime.utcnow() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode = {
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.SECURITY_ALGORITHM)
    return encoded_jwt

def login_required(http_authorization_credentials=Depends(HTTPBearer(scheme_name='Authorization'))):
    try:
        payload = jwt.decode(
            http_authorization_credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.SECURITY_ALGORITHM]
        )
        exp_time = datetime.utcfromtimestamp(payload.get("exp"))
        if exp_time < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"token expired",
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials",
        )



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
