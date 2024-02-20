from fastapi import Depends, APIRouter, status, Query, Body
from sqlalchemy.orm import Session
from app.crud import student_crud

from app.dependencies import get_db, user_email, user

from app.schemas import student_schemas
from app.routers.common_schemas import *

router = APIRouter(prefix="/student", tags=["Student"])

@router.get(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[student_schemas.Student],
)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(student_crud.get_student_by_email(db, token_email, student_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[student_schemas.Student],
)
async def student(
    list_id: int = Query(..., alias="listId"),
    student: student_schemas.StudentCreate = Body(...),
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(student_crud.create_student(db, token_email, list_id, student))


@router.put(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[student_schemas.Student],
)
async def student(
    student_id: int,
    student: student_schemas.StudentUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(student_crud.update_student(db, token_email, student_id, student))


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(student_crud.delete_student(db, token_email, student_id))
