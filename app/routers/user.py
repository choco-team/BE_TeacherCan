from fastapi import Depends, HTTPException, APIRouter, Request, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

import environ

from .. import crud, schemas
from ..dependencies import get_db

# 환경변수 init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

router = APIRouter(prefix="/user", tags=["User"])


# swagger ui 헤더에 jwt 추가를 위한 스키마
auth_scheme = HTTPBearer()


# 1.개인 정보 조회
@router.get("/info", status_code=200, response_model=schemas.User)
async def my_info(
    request: Request, db: Session = Depends(get_db), _: str = Depends(auth_scheme)
):
    db_user = crud.get_user(db, email=request.state.email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Token"
        )
    return db_user


# 2.개인 정보 수정
@router.put("/info", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def my_info(
    request: Request,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(auth_scheme),
):
    db_user = crud.update_user(db, email=request.state.email, user=user)
    return db_user
