from datetime import datetime
from pydantic import BaseModel, constr, Field
from typing import Optional
from enum import Enum
from pydantic_mongo import ObjectIdField


class Visible(str, Enum):
    Public = 'Public'
    Private = 'Private'


class Roles(str, Enum):
    Admin = 'Admin'
    Guest = 'Guest'


class BaseBoard(BaseModel):
    name: constr(min_length=3, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)] = Field(None)
    visible: Visible
    columns: list
    company: str


class Board(BaseBoard):
    id: ObjectIdField = Field(alias='_id')
    created_at: datetime
    users: list


class BoardUsers(BaseModel):
    id: str
    role: Roles
