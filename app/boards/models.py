from datetime import datetime
from pydantic import BaseModel, constr, Field
from typing import Optional
from enum import Enum
from app.core import ApiModel
from app.tasks import Task


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


class BoardTasks(BaseModel):
    name: str


class BoardUsers(ApiModel):
    role: Roles


class Board(BaseBoard, ApiModel):
    created_at: datetime
    users: list[BoardUsers]
    task_list: list[Task]