from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# User
class Result(BaseModel):
    result: bool
    message: str


class Token(Result):
    token: str


class UserBase(BaseModel):
    email: EmailStr


class UserSignin(UserBase):
    password: str


class UserCreate(UserSignin):
    nickname: str


class User(UserBase):
    social_id: str | None = Field(None, serialization_alias="socialId")
    nickname: str | None = Field(None)
    is_male: bool | None = Field(None, serialization_alias="isMale")
    birthday: date | None = Field(None)
    last_login: datetime | None = Field(None, serialization_alias="lastLogin")
    joined_at: datetime = Field(serialization_alias="joinedAt")
    avatar_sgv: str | None = Field(None, serialization_alias="avatarSgv")
    school: Optional["School"] = Field(None)

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    social_id: str | None = ...
    nickname: str | None = ...
    is_male: bool | None = ...
    birthday: date | None = ...
    last_login: datetime | None = ...
    avatar_sgv: str | None = ...
    school_id: str | None = ...

    model_config = ConfigDict(from_attributes=True)


class UserDelete(UserBase):
    pass


class SchoolBase(BaseModel):
    code: str


class School(SchoolBase):
    area_code: str | None = Field(None, serialization_alias="areaCode")
    name: str
    # users: list[User] = []

    model_config = ConfigDict(from_attributes=True)


class UserSchool(User):
    school: School = None


class SchoolList(BaseModel):
    schoolName: str = Field(alias="SCHUL_NM")
    schoolAddress: str = Field(alias="ORG_RDNMA")
    schoolCode: str = Field(alias="SD_SCHUL_CODE")
    areaCode: str = Field(alias="ATPT_OFCDC_SC_CODE")


class Pagination(BaseModel):
    pageNumber: int
    dataSize: int
    totalPageNumber: int | None


class SchoolLists(BaseModel):
    schoollist: list[SchoolList] | None
    pagination: Pagination


# Lunch Menu


class Menu(BaseModel):
    dish: str
    allergy: list[int]


class Origin(BaseModel):
    ingredient: str
    place: str


class SchoolMeal(BaseModel):
    meal_type: str
    date: date
    menu: list[Menu]
    origin: list[Origin]


User.model_rebuild()
