from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.schemas import student_schemas

class ColumnBase(BaseModel):
    field: str = Field(...)

class Column(ColumnBase):
    id: int = Field(...)

class Row(BaseModel):
    id: int = Field(...)
    value: str | None = Field(None)

class StudentList(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    description: str | None
    is_main: bool = Field(..., serialization_alias="isMain")
    has_allergy: bool = Field(False, serialization_alias="hasAllergy")
    created_at: datetime = Field(..., serialization_alias="createdAt")
    updated_at: datetime = Field(..., serialization_alias="updatedAt")

    model_config = ConfigDict(from_attributes=True)

class GetStudentList(BaseModel):
    studentList: list[StudentList]

class StudentWithRows(student_schemas.Student):
    id: int = Field(...)
    rows: list[Row] = Field([])

    model_config = ConfigDict(from_attributes=True)

class StudentListWithStudent(StudentList):
    columns: list[Column]
    students: list[StudentWithRows]

    model_config = ConfigDict(from_attributes=True)

class StudentListCreate(BaseModel):
    name: str
    description: str
    # has_allergy: bool = Field(False, alias="allergyYn")
    students: list[student_schemas.StudentCreate]

class UpdateMain(BaseModel):
    id: int
    is_main: bool | None = Field(True, alias="isMain")

class StudentListUpdate(BaseModel):
    id: int
    name: str
    description: str
    is_main: bool | None = Field(False, alias="isMain")
    # has_allergy: bool = Field(False, alias="hasAllergy")
    columns: list[Column]
    students: list[student_schemas.StudentUpdate]

# class ColumnUpdate(ColumnCreate):
#     value: list[str]

# class StudentListDelete(BaseModel):
#     id: int = Field(...)
