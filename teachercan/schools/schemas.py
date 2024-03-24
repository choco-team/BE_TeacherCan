from datetime import date
from enum import Enum

from ninja import Schema, Field


class DayOrWeek(str, Enum):
    day = "day"
    week = "week"


class SchoolOut(Schema):
    schoolName: str = Field(..., alias="name")
    schoolAddress: str = Field(..., alias="address")
    schoolCode: str = Field(..., alias="code")
    areaCode: str = Field(..., alias="area_code")


class SchoolIn(Schema):
    school_name: str = Field(..., alias="schoolName")
    page_number: int = Field(1, alias="pageNumber")
    data_size: int = Field(10, alias="dataSize")


class PaginationOut(Schema):
    pageNumber: int = Field(..., alias="page_number")
    dataSize: int = Field(..., alias="data_size")
    totalPageNumber: int = Field(..., alias="total_page_number")


class SchoolListOut(Schema):
    schoolList: list[SchoolOut] = Field(alias="school_list")
    pagination: PaginationOut


class LunchIn(Schema):
    type: DayOrWeek = Field(...)
    date: date


class MenuOut(Schema):
    dish: str
    allergy: list[int] = Field([])


class OriginOut(Schema):
    ingredient: str
    place: str


class LunchOut(Schema):
    mealType: str = Field(..., alias="meal_type")
    date: date
    menu: list[MenuOut]
    origin: list[OriginOut]
