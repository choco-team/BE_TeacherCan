from datetime import date, datetime
from typing import Optional, ForwardRef

from pydantic import BaseModel, EmailStr

User = ForwardRef("User")


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
    social_id: str | None = None
    nickname: str | None = None
    is_male: bool | None = None
    birthday: date | None = None
    last_login: datetime | None = None
    joined_at: datetime
    avatar_sgv: str | None = None
    school: Optional["School"] = None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    social_id: str | None = ...
    nickname: str | None = ...
    is_male: bool | None = ...
    birthday: date | None = ...
    avatar_sgv: str | None = ...
    school_code: str | None = ...


class UserDelete(UserBase):
    pass


class School(BaseModel):
    code: str
    area_code: str
    name: str
    # users: list[User] = []

    class Config:
        orm_mode = True


class UserSchool(User):
    school: School = None


class SchoolList(BaseModel):
    schoolName: str
    schoolAddress: str
    schoolCode: str
    areaCode: str


class Pagination(BaseModel):
    pageNumber: int
    dataSize: int
    totalPageNumber: int | None


class SchoolLists(BaseModel):
    schoollist: list[SchoolList] = None
    pagination: Pagination


class LunchMenu(BaseModel):
    menu: str
    allergy: list[int]


class Origin(BaseModel):
    ingredient: str
    origin: str


class SchoolLunch(BaseModel):
    lunchMenu: list[LunchMenu]
    origins: list[Origin]


User.update_forward_refs()
