from datetime import datetime, timedelta
from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.database import users
from jose import JWTError, jwt
from app.user import Token
from bson import ObjectId

# token var

SECRET_KEY = "09d25e054faa6ca2552c818166b7a9563b93f7091f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

# crypto var
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

exception = HTTPException(
                status_code=400,
                detail=[{"error": f'not a valid id, it must be a 12-byte input or a 24-character hex string'}]
            )

user_exception = HTTPException(
                status_code=400,
                detail=[{"error": f'User not found'}]
            )


async def get_password_hash(password):
    return pwd_context.hash(password)  # хешируем пароль


async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)  # сравниваем введенный пароль с хешированным


async def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# main logic
async def add_new_user(data):
    if await find_user_by_email(data.email):
        raise HTTPException(
            status_code=400,
            detail=[{"error": f'Пользователь с email: {data.email} уже существует'}]
        )
    user_for_insert = {
        'username': data.username,
        'password_hash': await get_password_hash(data.password.get_secret_value()),
        'email': data.email
    }
    await users.insert_one(user_for_insert)
    return {"message": f'Пользователь: {data.username} успешно зарегистрирован!'}


async def find_user_by_email(email):
    return await users.find_one({"email": email})


async def login_user_by_email(data):
    user = await find_user_by_email(data.username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=[{"error": f'Пользователь с email: {data.username} не существует'}]
        )
    elif not await verify_password(data.password, user["password_hash"]):
        raise HTTPException(
            status_code=403,
            detail=[{"error": 'Неверный пароль'}]
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await find_user_by_email(email=username)
    if user is None:
        raise credentials_exception
    return user["_id"]


async def verify_user(user_id_from_db, user_id):
    if user_id_from_db != user_id:
        raise HTTPException(
            status_code=403,
            detail=[{"error": 'Доступ запрещен'}]
        )
    return True


async def delete_user_by_email(email, user_id):
    try:
        user = await find_user_by_email(email)
        _id = user['_id']
        username = user['username']
        if verify_user(_id, user_id):
            await users.delete_one({"_id": ObjectId(_id)})
            return {"message": f'Пользователь {username} удален'}
    except TypeError:
        raise user_exception

