from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.user import CreateUser, UserLogIn, add_new_user, login_user_by_email, Token, get_current_user


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post("/create")
def registration_user(user: CreateUser):
    return add_new_user(user)


@router.post("/login", response_model=Token)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_user_by_email(form_data)


@router.get("/users/me/", response_model=CreateUser)
async def read_users_me(
    current_user: Annotated[CreateUser, Depends(get_current_user)]
):
    return current_user
