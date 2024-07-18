import email
from fastapi import status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

import jwt
from jwt.exceptions import InvalidTokenError

from auth.shemas import Token, TokenData, User, UserRegistration, UserInDB 
from config import SECRET_KEY
from auth.models import user
from db import get_async_session
# from auth.shemas import 


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db:AsyncSession, username: str):
    query = select(user).where(user.c.username == username)
    result = await db.execute(query)
    user_ = result.fetchone()
    if user_:
        return UserInDB(
            username=user_.username,
            email=user_.email,
            hashed_password=user_.hashed_password
        )


async def register_user(db:AsyncSession, user_reg:UserRegistration):
    user_dict = user_reg.dict()
    hashed_password = get_password_hash(user_dict['password'])
    query = insert(user).values(
        username = user_dict['username'],
        email = user_dict['email'],
        hashed_password = hashed_password
    )
    await db.execute(query)
    await db.commit()


async def authenticate_user(db:AsyncSession, username: str, password: str):
    user_ = await get_user(db, username)
    if not user_:
        return False
    if not verify_password(password, user_.hashed_password):
        return False
    return user_


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db:AsyncSession= Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if not current_user:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user