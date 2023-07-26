from fastapi import HTTPException
from passlib.context import CryptContext
from app.database import users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def add_new_user(data):
    if find_user_by_email(data.email):
        raise HTTPException(
            status_code=400,
            detail=[{"error": f'Пользователь с email: {data.email} уже существует'}]
        )
    user_for_insert = {
        'username': data.username,
        'password_hash': get_password_hash(data.password.get_secret_value()),
        'email': data.email
    }
    users.insert_one(user_for_insert)
    return {"data": f'Пользователь: {data.username} успешно зарегистрирован!'}


def find_user_by_email(email):
    return users.find_one({"email": email})
