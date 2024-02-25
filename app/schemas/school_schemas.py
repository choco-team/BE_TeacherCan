from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class SchoolBase(BaseModel):
    code: str
    
class School(SchoolBase):
    area_code: str | None = Field(None, serialization_alias="areaCode")
    name: str

    model_config = ConfigDict(from_attributes=True)

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