from datetime import date
from enum import Enum

from ninja import Schema, Field


class DayOrWeek(str, Enum):
    day = "day"
    week = "week"


class SchoolIn(Schema):
    schoolName: str = Field(..., alias="school_name")
    pageNumber: int = Field(1, alias="page_number")
    dataSize: int = Field(10, alias="data_size")


class LunchIn(Schema):
    type: DayOrWeek = Field(...)
    date: date
