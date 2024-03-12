from typing import Optional
from datetime import date, datetime
from enum import Enum
from ninja import Schema, Field

from ..schools.schemas import SchoolOut


class Gender(str, Enum):
    남 = "남"
    여 = "여"


class InfoIn(Schema):
    social_id: Optional[str] = Field(None, alias="socialId")
    nickname: Optional[str] = Field(None)
    gender: Optional[Gender] = Field(None)
    birthday: Optional[date] = Field(None)
    avatar_sgv: Optional[str] = Field(None, alias="avatarSgv")
    school_code: Optional[str] = Field(None, alias="schoolCode")


class InfoOut(Schema):
    email: str
    socialId: Optional[str] = Field(None, alias="social_id")
    nickname: Optional[str] = Field(None)
    gender: Optional[Gender] = Field(None)
    birthday: Optional[date] = Field(None)
    lastLogin: Optional[datetime] = Field(None, alias="last_login")
    joinedAt: datetime = Field(alias="joined_at")
    avatarSgv: Optional[str] = Field(None, alias="avatar_sgv")
    school: Optional[SchoolOut] = Field(None)
