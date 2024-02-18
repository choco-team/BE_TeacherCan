from pydantic import BaseModel, ConfigDict, validator

class BaseColumn (BaseModel):
    field: str

class column (BaseColumn):
    id: int


class PostColumnReq(BaseColumn):
    studentListId: int

class PostColumnRes(BaseModel):
    column_id: int

class GetColumnRes(BaseModel):
    columns: list[column]

    model_config = ConfigDict(from_attributes=True)
