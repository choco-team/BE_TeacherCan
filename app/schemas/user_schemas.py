from app.models import Gender

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.routers.school_router import school_schemas


class UserBase(BaseModel):
    email: EmailStr


class UserSignin(UserBase):
    password: str


class UserCreate(UserSignin):
    nickname: str


class User(UserBase):
    social_id: str | None = Field(None, serialization_alias="socialId")
    nickname: str | None = Field(None)
    gender: Gender | None = Field(None)
    birthday: date | None = Field(None)
    last_login: datetime | None = Field(None, serialization_alias="lastLogin")
    joined_at: datetime = Field(serialization_alias="joinedAt")
    avatar_sgv: str | None = Field(None, serialization_alias="avatarSgv")
    school: Optional["school_schemas.School"] = Field(None)

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    nickname: str = Field(...)
    social_id: str | None = Field(..., alias="socialId")
    is_male: bool | None = Field(..., alias="isMale")
    birthday: date | None = Field(...)
    avatar_sgv: str | None = Field(..., alias="avatarSgv")
    school_id: str | None = Field(..., alias="schoolCode")

    model_config = ConfigDict(from_attributes=True)


class UserDelete(UserBase): ...


User.model_rebuild()
