from fastapi import Depends, APIRouter

from app.dependencies import *
from app.routers.column.column_crud import *
from app.routers.column.column_schema import *

from app.routers.studentList.studentList_crud import get_student_list
from app.routers.student.student_crud import get_student
from app.routers.row.row_crud import create_row
from app.routers.common_schemas import *
from starlette import status


router = APIRouter(prefix="/column", tags=["Column"])

@router.get('/list/{studentListId}', response_model=ResponseModel[list[ColumnWithId]])
async def get_colomn_list_router(studentListId: int, db = Depends(get_verified_db)):
    columns = read_column_list(db, studentListId)
    return ResponseWrapper(columns)



@router.post('/', response_model=ResponseModel[PostColumnRes])
async def post_column_router(postColumn: PostColumnReq,  db = Depends(get_verified_db)):
    column = create_column(
        db=db, 
        student_list=get_student_list(db, postColumn.studentListId),  
        field=postColumn.field
    )
    for student in get_student(db, postColumn.studentListId):
        create_row(
            db=db,
            student=student,
            column=column
        )
    return ResponseWrapper(PostColumnRes(column_id=column.id))

@router.put('/', response_model=ResponseModel[str])
async def put_column_router(column_update: ColumnWithId,  db = Depends(get_verified_db)):
    update_column(
        db = db,
        column_update = column_update
    )
    return ResponseWrapper("성공적으로 수정되었어요.")


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_column_router(id: int,  db = Depends(get_verified_db)):
    delete_column(db=db, column_id = id)
