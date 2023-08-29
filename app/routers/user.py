from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..dependencies import get_db
from .auth import verify_token

router = APIRouter(prefix="/user", tags=["User"])


# 1.개인 정보 조회
@router.get("/info", status_code=200, response_model=schemas.User)
async def my_info(
    db: Session = Depends(get_db), token_email: str = Depends(verify_token)
):
    db_user = crud.get_user(db, email=token_email)
    return db_user


# 2.개인 정보 수정
@router.put("/info", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def my_info(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    db_user = crud.update_user(db, email=token_email, user=user)
    return db_user
