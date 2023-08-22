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
    nickname: str = Field(..., alias="nickname")
    social_id: str | None = Field(..., alias="socialId")
    is_male: bool | None = Field(..., alias="isMale")
    birthday: date | None = Field(..., alias="birthday")
    last_login: datetime | None = Field(..., alias="lastLogin")
    avatar_sgv: str | None = Field(..., alias="avatarSgv")
    school_id: str | None = Field(..., alias="schoolCode")

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
    school_name: str = Field(alias="SCHUL_NM", serialization_alias="schoolName")
    school_address: str = Field(alias="ORG_RDNMA", serialization_alias="schoolAddress")
    school_code: str = Field(alias="SD_SCHUL_CODE", serialization_alias="schoolCode")
    area_code: str = Field(alias="ATPT_OFCDC_SC_CODE", serialization_alias="areaCode")


class Pagination(BaseModel):
    page_number: int = Field(serialization_alias="pageNumber")
    data_size: int = Field(serialization_alias="dateSize")
    total_page_number: int = Field(serialization_alias="totalPageNumber")


class SchoolLists(BaseModel):
    school_list: list[SchoolList] = Field(serialization_alias="schoolList")
    pagination: Pagination


# Lunch Menu


class Menu(BaseModel):
    dish: str
    allergy: list[int]


class Origin(BaseModel):
    ingredient: str
    place: str


class SchoolMeal(BaseModel):
    meal_type: str = Field(..., serialization_alias="mealType")
    date: date
    menu: list[Menu]
    origin: list[Origin]


User.model_rebuild()
