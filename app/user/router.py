from fastapi import APIRouter
from app.user import CreateUser, UserLogIn, add_user


router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post("/create")
def add_new_user(user: CreateUser):
    return add_user(user.model_dump())


# @router.post("/login")
# def login_user(login: UserLogIn):
#     encode_user = jsonable_encoder(login)
#     result = find_user(encode_user["email"])
#     return {"data": result}