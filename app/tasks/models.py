from bson import ObjectId
from pydantic import BaseModel, constr, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ApiModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId(), alias='_id')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class State(str, Enum):
    Created = 'Created'
    Finished = 'Finished'


class Task(ApiModel):
    name: constr(min_length=3, max_length=255)
    description: constr(min_length=0, max_length=255)
    deadline: datetime
    state: str
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
