from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.user import User, add_new_user, login_user_by_email, Token, get_current_user


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post("/create")
def registration_user(user: User):
    return add_new_user(user)


@router.post("/login", response_model=Token)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_user_by_email(form_data)


@router.get("/me")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user['email']
