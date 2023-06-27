from datetime import datetime, timedelta
from typing import Union, Any
from models.auth_model.auth_model import PayloadToken, UserView
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from starlette import status
from passlib.context import CryptContext
from repository.user_db_manager.user_db_manager import UserDbManager
from service.parser import ParseEnv

base_auth = OAuth2PasswordBearer(
    tokenUrl="api/v1/user/signin",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(base_auth)):
    try:
        payload = jwt.decode(
            token,
            ParseEnv.JWT_SECRET_KEY,
            algorithms=ParseEnv.ALGORITHM
        )
        token_data = PayloadToken(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserDbManager.get_user_from_db(username=token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return UserView(**user)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(ParseEnv.ACCESS_TIME))
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, ParseEnv.JWT_SECRET_KEY, ParseEnv.ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=int(ParseEnv.REFRESH_TIME))

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, ParseEnv.JWT_REFRESH_KEY, ParseEnv.ALGORITHM)
    return encoded_jwt


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)
