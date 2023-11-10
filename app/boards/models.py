from datetime import datetime
from pydantic import BaseModel, constr, Field
from typing import Optional
from enum import Enum
from app.core import ApiModel


class Visible(str, Enum):
    Public = 'Public'
    Private = 'Private'


class BaseBoard(BaseModel):
    name: constr(min_length=3, max_length=255)
    description: Optional[constr(min_length=0, max_length=255)] = Field(None)
    visible: Visible
    columns: list
    company: str


class Board(BaseBoard, ApiModel):
    _id: ApiModel
    created_at: datetime
