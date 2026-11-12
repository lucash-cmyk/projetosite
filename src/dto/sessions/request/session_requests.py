from pydantic import BaseModel, Field, field_validator

from dto.shared.email import normalize_email


class LoginRequest(BaseModel):
    email: str
    password: str = Field(min_length=1)

    @field_validator("email")
    @classmethod
    def _email(cls, value):
        return normalize_email(value)


class UserIdRequest(BaseModel):
    user_id: str = Field(min_length=1)


class SessionIdRequest(BaseModel):
    session_id: str = Field(min_length=1)
