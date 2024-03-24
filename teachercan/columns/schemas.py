from ninja import Schema, Field

class BaseColumn (Schema):
    field: str

class ColumnWithId (BaseColumn):
    id: int

class GetColumnRes (Schema):
    columns: list[ColumnWithId]

class PostColumnReq(BaseColumn):
    student_list_id: int = Field(..., alias="studentListId")