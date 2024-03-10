from typing import Optional
from datetime import date, datetime
from enum import Enum
from ninja import Schema, Field

from ..schools.schemas import SchoolOut


class Gender(str, Enum):
    남 = "남"
    여 = "여"


class InfoIn(Schema):
    social_id: str | None = Field(None, alias="socialId")
    nickname: str | None = Field(None)
    gender: Gender | None = Field(None)
    birthday: date | None = Field(None)
    avatar_sgv: str | None = Field(None, alias="avatarSgv")
    school_code: str | None = Field(None, alias="schoolCode")


class InfoOut(Schema):
    email: str
    socialId: str | None = Field(None, alias="social_id")
    nickname: str | None = Field(None)
    gender: Gender | None = Field(None)
    birthday: date | None = Field(None)
    lastLogin: datetime | None = Field(None, alias="last_login")
    joinedAt: datetime = Field(alias="joined_at")
    avatarSgv: str | None = Field(None, alias="avatar_sgv")
    school: Optional[SchoolOut] = Field(None)
