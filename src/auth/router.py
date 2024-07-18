from fastapi import APIRouter,HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from auth.shemas import Token, UserRegistration, User
from auth.depends import create_access_token, authenticate_user, register_user, get_current_user
from db import get_async_session


ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter(
    tags=['auth']
)

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> Token:
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register")
async def registration(
    user:UserRegistration,
    session: AsyncSession = Depends(get_async_session)
):
    await register_user(session, user)
    return {'status':'added'}





