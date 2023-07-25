from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.mongo_db_script import add_new_user, find_user
from app.user import CreateUser, UserLogIn

router = APIRouter(
    prefix='/user',
    tags=['User']
)


# пока ручки болванки
@router.post("/create")
def add_user(user: CreateUser):
    encode_user = user.dict()
    add_new_user(encode_user)
    return {"data": "Вы успешно зарегистрированы"}


@router.post("/login")
def login_user(login: UserLogIn):
    encode_user = jsonable_encoder(login)
    result = find_user(encode_user["email"])
    return {"data": result}