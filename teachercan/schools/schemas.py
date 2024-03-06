from enum import Enum

from ninja import Schema, Field


# class DayOrWeek(Enum):


class SchoolIn(Schema):
    schoolName: str = Field(..., alias="school_name")
    pageNumber: int = Field(1, alias="page_number")
    dataSize: int = Field(10, alias="data_size")
