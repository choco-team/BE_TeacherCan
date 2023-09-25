from fastapi import Depends, APIRouter, status, Query, Body
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..schemas import ResponseModel, ResponseWrapper
from ..dependencies import get_db, user_email

router = APIRouter(prefix="/student", tags=["Student"])


# 명렬표
@router.get(
    "/list", status_code=200, response_model=ResponseModel[list[schemas.StudentList]]
)
async def student_list(
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.get_student_lists(db, token_email))


@router.get(
    "/list/{list_id}",
    status_code=200,
    response_model=ResponseModel[schemas.StudentList],
)
async def student_list(
    list_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.get_student_list(db, token_email, list_id))


@router.post(
    "/list",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[schemas.StudentList],
)
async def student_list(
    student_list: schemas.StudentListCreate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.create_student_list(db, token_email, student_list))


@router.delete("/list/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def student_list(
    list_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.delete_student_list(db, token_email, list_id))


@router.put(
    "/list/{list_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.StudentList],
)
async def student_list(
    list_id: int,
    student_list: schemas.StudentListUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(
        crud.update_student_list(db, token_email, list_id, student_list)
    )


@router.get(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.Student],
)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.get_student(db, token_email, student_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[schemas.Student],
)
async def student(
    list_id: int = Query(..., alias="listId"),
    student: schemas.StudentCreate = Body(...),
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.create_student(db, token_email, list_id, student))


@router.put(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.Student],
)
async def student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.update_student(db, token_email, student_id, student))


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.delete_student(db, token_email, student_id))
