from pydantic import BaseModel, Field, ConfigDict

from app.models import Gender

class Row(BaseModel):
    id: int = Field(...)
    value: str | None = Field(None)

class Student(BaseModel):
    number: int = Field(..., serialization_alias="studentNumber")
    name: str = Field(..., serialization_alias="studentName")
    gender: Gender = Field(...)
    allergy: list[int] | None = Field(None)

    model_config = ConfigDict(from_attributes=True)

class StudentCreate(BaseModel):
    number: int = Field(..., alias="studentNumber")
    name: str = Field(..., alias="studentName")
    gender: Gender = Field(...)

class StudentUpdate(BaseModel):
    id: int = Field(...)
    number: int = Field(..., alias="studentNumber")
    name: str = Field(..., alias="studentName")
    gender: Gender = Field(...)
    allergy: list[int] | None = Field(None)
    rows: list[Row] = Field([])

    model_config = ConfigDict(from_attributes=True)

# class StudentDelete(BaseModel):
#     id: int = Field(...)