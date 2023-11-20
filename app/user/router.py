from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.user import UserPassword, add_new_user, login_user_by_email, Token, get_current_user, delete_user_by_email, MessageResponse

router = APIRouter(
    prefix='/user',
    tags=['User']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create", response_model=MessageResponse)
async def registration_user(user: UserPassword):
    return await add_new_user(user)


@router.post("/login", response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login_user_by_email(form_data)


@router.delete("/delete", response_model=MessageResponse)
async def delete_user(email, auth: Auth):
    return await delete_user_by_email(email, auth)
