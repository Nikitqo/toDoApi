from bson.objectid import ObjectId
from pydantic import BaseModel, constr, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from app.core import ApiModel


class State(str, Enum):
    Created = 'Created'
    Finished = 'Finished'


class Task(ApiModel):
    _id: ObjectId
    name: constr(min_length=3, max_length=255)
    description: constr(min_length=0, max_length=255)
    deadline: datetime
    state: State
    created_at: datetime


class CreateTask(BaseModel):
    name: constr(min_length=3, max_length=255)
    description: constr(min_length=0, max_length=255)
    deadline: datetime


class UpdateTask(BaseModel):
    name: Optional[constr(min_length=3, max_length=255)]
    description: Optional[constr(min_length=0, max_length=255)]
    deadline: Optional[datetime]
    state: Optional[State]


class MessageResponse(BaseModel):
    message: str
