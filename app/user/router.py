from fastapi import APIRouter
from app.user import CreateUser, UserLogIn, add_new_user, login_user_by_email, Token


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post("/create")
def registration_user(user: CreateUser):
    return add_new_user(user)


@router.post("/login", response_model=Token)
def login_user(credentials: UserLogIn):
    return login_user_by_email(credentials)
