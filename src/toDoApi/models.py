from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: constr(min_length=8, max_length=16)


class UserLogIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=16)


class CreateTask(BaseModel):
    name: constr(min_length=3, max_length=255)
    description: constr(min_length=0, max_length=255)
    deadline: datetime


class UpdateTask(BaseModel):
    name: Optional[constr(min_length=3, max_length=255)]
    description: Optional[constr(min_length=0, max_length=255)]
    deadline: Optional[datetime]
    state: Optional[str]
