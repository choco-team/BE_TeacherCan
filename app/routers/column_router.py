from fastapi import Depends, APIRouter
from app.crud import column_crud

from app.dependencies import *
from app.schemas import column_schema

from app.crud import studentList_crud
from app.crud import student_crud
from app.crud import row_crud

from app.routers.common_schemas import *
from starlette import status


router = APIRouter(prefix="/column", tags=["Column"])

@router.get('/list/{studentListId}', response_model=ResponseModel[list[column_schema.ColumnWithId]])
async def get_colomn_list_router(studentListId: int, db = Depends(get_verified_db)):
    columns = column_crud.read_column_list(db, studentListId)
    return ResponseWrapper(columns)



@router.post('', response_model=ResponseModel[column_schema.PostColumnRes])
async def post_column_router(postColumn: column_schema.PostColumnReq,  db = Depends(get_verified_db)):
    column = column_crud.create_column(
        db=db, 
        student_list=studentList_crud.get_student_list_asd(db, postColumn.studentListId),  
        field=postColumn.field
    )
    for student in student_crud.get_student(db, postColumn.studentListId):
        row_crud.create_row(
            db=db,
            student=student,
            column=column
        )
    return ResponseWrapper(column_schema.PostColumnRes(column_id=column.id))

@router.put('', response_model=ResponseModel[str])
async def put_column_router(column_update: column_schema.ColumnWithId,  db = Depends(get_verified_db)):
    column_crud.update_column(
        db = db,
        column_update = column_update
    )
    return ResponseWrapper("성공적으로 수정되었어요.")


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_column_router(id: int,  db = Depends(get_verified_db)):
    column_crud.delete_column(db=db, column_id = id)
