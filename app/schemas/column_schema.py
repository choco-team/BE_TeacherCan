from pydantic import BaseModel

class BaseColumn (BaseModel):
    field: str

class ColumnWithId (BaseColumn):
    id: int


class PostColumnReq(BaseColumn):
    studentListId: int

class PostColumnRes(BaseModel):
    column_id: int

class GetColumnRes(BaseModel):
    columns: list[ColumnWithId]