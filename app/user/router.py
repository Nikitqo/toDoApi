from fastapi import APIRouter
from app.user import CreateUser, UserLogIn, add_new_user


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post("/create")
def registration_user(user: CreateUser):
    return add_new_user(user)


# @router.post("/login")
# def login_user(login: UserLogIn):
#     encode_user = jsonable_encoder(login)
#     result = find_user(encode_user["email"])
#     return {"data": result}