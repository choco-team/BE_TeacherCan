from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password

from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

import environ
import jwt

from .. import crud, schemas
from ..dependencies import get_db

# 환경변수 init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

router = APIRouter(prefix="/auth", tags=["Auth"])


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
    db_user = schemas.UserUpdate.from_orm(db_user)
    db_user.last_login = datetime.utcnow()
    crud.update_user(db, email=user.email, user=db_user)

    # Create jwt
    token = jwt.encode(
        {"email": user.email, "exp": datetime.utcnow() + timedelta(hours=24)},
        env("JWT_SECRET"),
        env("JWT_ALGORITHM"),
    )

    return {"result": True, "message": "Success Login", "token": token}
