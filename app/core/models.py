from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field
from pydantic_mongo import ObjectIdField


class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class ApiModel(BaseModel):
    id: ObjectIdField = Field(alias='_id')
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})