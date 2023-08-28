from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password

from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

import jwt

from .. import crud, schemas
from ..dependencies import get_db

from ..common.consts import JWT_ALGORITHM, JWT_SECRET

router = APIRouter(prefix="/auth", tags=["Auth"])

# swagger ui 헤더에 jwt 추가를 위한 스키마
auth_scheme = HTTPBearer()


# Auth
# 1.이메일 중복검사
@router.post("/signup/validation", status_code=200, response_model=schemas.Result)
def is_email_usable(user: schemas.UserBase, db: Session = Depends(get_db)):
    """
    `이메일 중복검사`
    """
    db_user = crud.get_user(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="The email is already in use.")
    return {"result": True, "message": "The email is available."}


# 2.회원가입
@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    `회원가입`
    """
    crud.create_user(db, user=user)


# 3.로그인
@router.post("/signin", status_code=200, response_model=schemas.Token)
def signin(user: schemas.UserSignin, db: Session = Depends(get_db)):
    """
    `로그인`
    """
    db_user = crud.get_user(db, email=user.email)
    if db_user is None or not check_password(user.password, db_user.password):
        raise HTTPException(
            status_code=400, detail={"result": False, "message": "Failed Login"}
        )

    # Edit last_login
    setattr(db_user, "last_login", datetime.utcnow())
    db.commit()
    db.refresh(db_user)

    # Create jwt
    token = jwt.encode(
        {"email": user.email, "exp": datetime.utcnow() + timedelta(hours=24)},
        JWT_SECRET,
        JWT_ALGORITHM,
    )

    return {"result": True, "message": "Success Login", "token": token}
