from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


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
    id: int
    social_id: Optional[str] = None
    nickname: Optional[str] = None
    is_male: Optional[bool] = None
    birthday: Optional[date] = None
    last_login: Optional[datetime] = None
    joined_at: datetime
    avatar_sgv: Optional[str] = None
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


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
