from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.user import User, add_new_user, login_user_by_email, Token, get_current_user, delete_user_by_email

router = APIRouter(
    prefix='/user',
    tags=['User']
)

Auth = Annotated[dict, Depends(get_current_user)]


@router.post("/create")
def registration_user(user: User):
    return add_new_user(user)


@router.post("/login", response_model=Token)
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return login_user_by_email(form_data)


@router.delete("/delete")
def delete_user(email, auth: Auth):
    return delete_user_by_email(email, auth)
