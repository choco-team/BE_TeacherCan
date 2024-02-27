from datetime import date, datetime
from enum import Enum
from ninja import Schema
from pydantic import Field


class Gender(str, Enum):
    남 = "남"
    여 = "여"


class InfoOut(Schema):
    email: str
    social_id: str | None = Field(None, serialization_alias="socialId")
    nickname: str | None = Field(None)
    gender: Gender | None = Field(None)
    birthday: date | None = Field(None)
    last_login: datetime | None = Field(None, serialization_alias="lastLogin")
    joined_at: datetime = Field(serialization_alias="joinedAt")
    avatar_sgv: str | None = Field(None, serialization_alias="avatarSgv")
    # school: Optional["school_schemas.School"] = Field(None)
