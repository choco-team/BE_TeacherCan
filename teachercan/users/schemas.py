from datetime import date, datetime
from enum import Enum
from ninja import Schema, Field


class Gender(str, Enum):
    남 = "남"
    여 = "여"


class InfoIn(Schema):
    socialId: str | None = Field(None, alias="social_id")
    nickname: str | None = Field(None)
    gender: Gender | None = Field(None)
    birthday: date | None = Field(None)
    avatarSgv: str | None = Field(None, alias="avatar_sgv")
    schoolCode: str | None = Field(None, alias="school_code")


class InfoOut(Schema):
    email: str
    socialId: str | None = Field(None, alias="social_id")
    nickname: str | None = Field(None)
    gender: Gender | None = Field(None)
    birthday: date | None = Field(None)
    lastLogin: datetime | None = Field(None, alias="last_login")
    joinedAt: datetime = Field(alias="joined_at")
    avatarSgv: str | None = Field(None, alias="avatar_sgv")
    # school: Optional["school_schemas.School"] = Field(None)
