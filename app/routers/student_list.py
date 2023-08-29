from fastapi import Depends, HTTPException, APIRouter, status, Query, Body
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db
from .auth import verify_token

router = APIRouter(prefix="/student", tags=["Student"])


# 명렬표
@router.get("/list", status_code=200, response_model=list[schemas.StudentList])
async def student_list(
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.get_student_lists(db, token_email)


@router.get("/list/{list_id}", status_code=200, response_model=schemas.StudentList)
async def student_list(
    list_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.get_student_list(db, token_email, list_id)


@router.post(
    "/list", status_code=status.HTTP_201_CREATED, response_model=schemas.StudentList
)
async def student_list(
    student_list: schemas.StudentListCreate,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.create_student_list(db, token_email, student_list)


@router.delete("/list/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def student_list(
    list_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.delete_student_list(db, token_email, list_id)


@router.put(
    "/list/{list_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.StudentList,
)
async def student_list(
    list_id: int,
    student_list: schemas.StudentListUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.update_student_list(db, token_email, list_id, student_list)


@router.get(
    "/{student_id}", status_code=status.HTTP_200_OK, response_model=schemas.Student
)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.get_student(db, token_email, student_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Student)
async def student(
    list_id: int = Query(..., alias="listId"),
    student: schemas.StudentCreate = Body(...),
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.create_student(db, token_email, list_id, student)


@router.put(
    "/{student_id}", status_code=status.HTTP_200_OK, response_model=schemas.Student
)
async def student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.update_student(db, token_email, student_id, student)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    return crud.delete_student(db, token_email, student_id)
