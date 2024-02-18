from fastapi import Depends, APIRouter

from app.dependencies import *
from app.routers.column.column_crud import *
from app.routers.column.column_schema import *

from app.routers.studentList.studentList_crud import get_student_list
from app.routers.student.student_crud import get_student
from app.routers.row.row_crud import create_row
from app.routers.common_schemas import *

router = APIRouter(prefix="/column", tags=["Column"])

@router.get('/list/{studentListId}', response_model=ResponseModel[list[column]])
async def get_colomn_list(studentListId: int, db = Depends(get_verified_db)):
    columns = get_columns(db, studentListId)
    print("asdasdasdasd", type(columns[0]))
    return ResponseWrapper(columns)



@router.post('/', response_model=ResponseModel[PostColumnRes])
async def post_column(postColumn: PostColumnReq,  db = Depends(get_verified_db)):
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

