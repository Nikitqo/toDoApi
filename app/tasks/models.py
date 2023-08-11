from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional
from enum import Enum


class State(str, Enum):
    Created = 'Created'
    Finished = 'Finished'


class CreateTask(BaseModel):
    name: constr(min_length=3, max_length=255)
    description: constr(min_length=0, max_length=255)
    deadline: datetime


class Task(BaseModel):
    id: str
    name: constr(min_length=3, max_length=255)
    description: constr(min_length=0, max_length=255)
    deadline: datetime
    state: str
    created_at: datetime


class UpdateTask(BaseModel):
    name: Optional[constr(min_length=3, max_length=255)]
    description: Optional[constr(min_length=0, max_length=255)]
    deadline: Optional[datetime]
    state: Optional[State]


class TaskList(BaseModel):
    data: list[Task]
