from datetime import datetime
from ninja import Schema, Field
from enum import Enum

class Gender(str, Enum):
    남 = "남"
    여 = "여"

class ColumnBase(Schema):
    field: str = Field(...)

class Column(ColumnBase):
    id: int = Field(...)

class Row(Schema):
    id: int = Field(...)
    value: str | None = Field(None)

class Student(Schema):
    number: int = Field(..., serialization_alias="studentNumber")
    name: str = Field(..., serialization_alias="studentName")
    gender: Gender = Field(...)
    allergy: list[int] | None = Field(None)

class StudentCreate(Schema):
    number: int = Field(..., alias="studentNumber")
    name: str = Field(..., alias="studentName")
    gender: Gender = Field(...)

class StudentUpdate(Schema):
    id: int = Field(...)
    number: int = Field(..., alias="StudentNumber")
    name: str = Field(..., alias="StudentName")
    gender: Gender = Field(...)
    allergy: list[int] | None = Field(None)
    rows: list[Row] = Field([])

class StudentList(Schema):
    id: int = Field(...)
    name: str = Field(...)
    is_main: bool = Field(..., serialization_alias="isMain")
    has_allergy: bool = Field(False, serialization_alias="hasAllergy")
    created_at: datetime = Field(..., serialization_alias="createdAt")
    updated_at: datetime = Field(..., serialization_alias="updatedAt")
    # columns: list[Column]
    # students: list[StudentWithRows]
class GetStudentList(Schema):
    studentList: list[StudentList]


class StudentWithRows(Student):
    id: int = Field(...)
    # rows: list[Row] = Field([])

class StudentListWithStudent(StudentList):
    # columns: list[Column]
    students: list[StudentWithRows]

class StudentListCreate(Schema):
    name: str
    description: str
    students: list[StudentCreate]


class UpdateMain(Schema):
    id: int
    isMain: bool


class StudentListUpdate(Schema):
    id: int = Field(...)
    name: str = Field(...)
    is_main: bool | None = Field(False, alias="isMain")
    has_allergy: bool = Field(False, alias="hasAllergy")
    columns: list[Column] = Field(...)
    students: list[StudentUpdate]
