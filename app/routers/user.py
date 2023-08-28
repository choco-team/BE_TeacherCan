from fastapi import Depends, HTTPException, APIRouter, Request, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db
from .auth import auth_scheme

router = APIRouter(prefix="/user", tags=["User"])


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


# TODO 명렬표
@router.get("/student")
async def test(db: Session = Depends(get_db)):
    return {"test": "test_result"}
