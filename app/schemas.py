from datetime import date, datetime
from typing import Optional, Generic, TypeVar, Type, Any, Union

from pydantic import BaseModel, EmailStr, Field, ConfigDict, create_model

T = TypeVar("T", bound=BaseModel)

# from functools import lru_cache

# @lru_cache()
# def get_standard_response_model(cls: Type[BaseModel]) -> Type[BaseModel]:
#     assert issubclass(cls, BaseModel)
#     return create_model(
#         f"StandardData[{cls.__name__}]",
#         result=(bool, True),
#         code=(int, 2000),
#         message=(str | None, None),
#         data=(cls | None, None),
#     )


class ResponseModel(Generic[T]):
    def __class_getitem__(cls, item):
        return create_model(
            f"StandardData[{item.__name__}]",
            result=(bool, True),
            code=(int, 2000),
            message=(str | None, None),
            data=(item | None, None),
        )
        # return get_standard_response_model(item)

    # def __new__(cls, data: Union[T, Type[T]]) -> "ResponseModel[T]":
    #     result: bool
    #     code: int
    #     message: str | None
    #     # noinspection PyUnusedLocal
    #     response_data: BaseModel | None
    #     if isinstance(data, BaseModel):
    #         response_type = get_standard_response_model(type(data))
    #         response_data = data
    #     else:
    #         assert issubclass(data, BaseModel)
    #         response_type = get_standard_response_model(data)
    #         response_data = None

    #     # noinspection PyTypeChecker
    #     return response_type(result=result, code=code, message=message, data=response_data)  # type: ignore


class ResponseWrapper(ResponseModel):
    def __init__(self, data):
        self.data = data


# User
class Result(BaseModel):
    result: bool
    message: str

    def __repr__(self):
        return f"Result(result:{self.result}, message:{self.message})"


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
    nickname: str = Field(...)
    social_id: str | None = Field(..., alias="socialId")
    is_male: bool | None = Field(..., alias="isMale")
    birthday: date | None = Field(...)
    avatar_sgv: str | None = Field(..., alias="avatarSgv")
    school_id: str | None = Field(..., alias="schoolCode")

    model_config = ConfigDict(from_attributes=True)


class UserDelete(UserBase):
    ...


class SchoolBase(BaseModel):
    code: str


class School(SchoolBase):
    area_code: str | None = Field(None, serialization_alias="areaCode")
    name: str

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
class Allergy(BaseModel):
    code: int
    name: str


class Menu(BaseModel):
    dish: str
    allergy: list[int] = Field([])


class Origin(BaseModel):
    ingredient: str
    place: str


class SchoolMeal(BaseModel):
    meal_type: str = Field(..., serialization_alias="mealType")
    date: date
    menu: list[Menu]
    origin: list[Origin]


User.model_rebuild()


# Student List
class StudentDelete(BaseModel):
    id: int = Field(...)


class StudentCreate(BaseModel):
    number: int = Field(...)
    name: str = Field(...)
    is_male: bool = Field(..., alias="isMale")
    description: str | None = Field(None)
    allergy: list[int] | None


class StudentUpdate(StudentCreate):
    ...


class Student(StudentDelete, StudentUpdate):
    is_male: bool = Field(serialization_alias="isMale")
    allergy: list[Allergy] = Field([])
    allergies: list[int] = Field([], serialization_alias="allergy")

    model_config = ConfigDict(from_attributes=True)


class StudentListDelete(BaseModel):
    id: int = Field(...)


class StudentListUpdate(BaseModel):
    name: str = Field(...)
    is_main: bool | None = Field(False, alias="isMain")


class StudentListCreate(StudentListUpdate):
    students: list[StudentCreate]


class StudentList(StudentListDelete, StudentListUpdate):
    is_main: bool = Field(..., serialization_alias="isMain")
    created_at: datetime = Field(..., serialization_alias="createdAt")
    updated_at: datetime = Field(..., serialization_alias="updatedAt")
    students: list[Student]

    model_config = ConfigDict(from_attributes=True)
