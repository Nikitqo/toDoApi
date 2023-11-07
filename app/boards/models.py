from bson import ObjectId
from pydantic import constr, BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum
from app.core import ApiModel


class Visible(str, Enum):
    Public = 'Public'
    Private = 'Private'


class Board(ApiModel):
    _id: ObjectId
    name: constr(min_length=3, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)]
    columns: list
    company: str
    visible: Visible
    created_at: datetime


class CreateBoard(BaseModel):
    name: constr(min_length=3, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)]
    visible: Visible
    columns: list
    company: str

