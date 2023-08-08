from fastapi import Body, Depends, HTTPException, APIRouter, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import Annotated

import environ

from .. import crud, schemas
from ..dependencies import get_db

# 환경변수 init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

router = APIRouter(prefix="/student", tags=["Student"])


# swagger ui 헤더에 jwt 추가를 위한 스키마
auth_scheme = HTTPBearer()


# 1. 학생등록
@router.post("/registrate", status_code=200, response_model=schemas.Result)
async def registrate_student(
    #request: Request, 
    email: Annotated[str, Body()], students:list[schemas.StudentCreate], db: Session = Depends(get_db), 
    #_: str = Depends(auth_scheme)
):
    db_user = crud.get_user(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자 정보가 없습니다."
        )
    crud.create_student(db, students, db_user.id)
    db_user = crud.get_user(db, email=email)
    print(db_user.students)
    return {"result": True, "message": "학생정보가 등록되었습니다."}