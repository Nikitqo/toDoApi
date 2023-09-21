from pydantic import BaseModel, EmailStr, SecretStr, validator


class User(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr

    @validator('password')
    def name_must_contain_space(cls, v):
        if len(v) < 8:
            raise ValueError('Your password must be at least 8 characters')
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class MessageResponse(BaseModel):
    message: str
