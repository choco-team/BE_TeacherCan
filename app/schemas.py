from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


# User
class Result(BaseModel):
    result: bool
    message: str


class Token(Result):
    token: str


class UserBase(BaseModel):
    user_id: str


class UserSignin(UserBase):
    password: str


class UserCreate(UserSignin):
    nickname: str


class User(UserBase):
    id: int
    social_id: Optional[str] = None
    email: Optional[str] = None
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
