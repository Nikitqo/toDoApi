from pydantic import BaseModel, EmailStr, SecretStr, field_validator


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr

    @field_validator('password')
    def name_must_contain_space(cls, v):
        if len(v) < 8:
            raise ValueError('Your password must be at least 8 characters')
        return v


class UserLogIn(BaseModel):
    email: EmailStr
    password: SecretStr
