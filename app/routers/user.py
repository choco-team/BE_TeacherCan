from typing import Annotated
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import (
    check_password
)

from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

import environ
import jwt

from .. import crud, schemas
from ..dependencies import get_db

# 환경변수 init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

router = APIRouter(prefix="/user", tags=["User"])


# swagger ui 헤더에 jwt 추가를 위한 스키마
auth_scheme = HTTPBearer()

# User
# 1.회원가입 - 1.이메일 중복검사
@router.post(
    "/auth/signup/validation",
    status_code=200,
    response_model=schemas.Result,
    responses={
        400: {
            "model": schemas.Result,
            "content": {
                "application/json": {
                    "example": {"result": False, "message": "error message"}
                }
            },
        }
    },
)
def is_email_usable(user: schemas.UserBase, db: Session = Depends(get_db)):
    """
    `이메일 중복검사`
    """
    db_user = crud.get_user(db, email=user.email)
    if db_user:
        return JSONResponse(
            status_code=400, content={"result": False, "message": "이미 가입된 이메일입니다."}
        )
        # raise HTTPException(
        #     status_code=400, detail={"result": False, "message": "이미 가입된 이메일입니다."}
        # )
    return {"result": True, "message": "회원가입이 가능한 이메일입니다."}


# 1.회원가입 - 2.회원가입
@router.post(
    "/auth/signup",
    status_code=200,
    response_model=schemas.Result,
    responses={
        400: {
            "model": schemas.Result,
            "content": {
                "application/json": {
                    "example": {"result": False, "message": "error message"}
                }
            },
        }
    },
)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    `회원가입`
    """
    db_user = crud.get_user(db, email=user.email)
    if db_user:
        return JSONResponse(
            status_code=400, content={"result": False, "message": "이미 가입된 이메일입니다."}
        )

    # password validation
    try:
        validate_password(user.password)
    except ValidationError as error:
        message = ""
        for error_message in error.messages:
            message = f"{message} {error_message}"
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["body", "password"],
                    "msg": message.lstrip(),
                    "type": "value_error.password",
                }
            ],
        )

    if crud.create_user(db, user=user):
        return {"result": True, "message": "회원가입이 완료되었습니다."}
    else:
        raise HTTPException(status_code=500)


# 2.로그인 - 1.로그인
@router.post("/auth/signin", status_code=200, response_model=schemas.Token)
def signin(user: schemas.UserSignin, db: Session = Depends(get_db)):
    """
    `로그인`
    """
    db_user = crud.get_user(db, email=user.email)
    if db_user is None or not check_password(user.password, db_user.password):
        raise HTTPException(
            status_code=400, detail={"result": False, "message": "로그인에 실패하였습니다."}
        )

    token = jwt.encode(
        {"email": user.email, "exp": datetime.utcnow() + timedelta(hours=24)},
        env("JWT_SECRET"),
        env("JWT_ALGORITHM"),
    )

    return {"result": True, "message": "로그인 되었습니다.", "token": token}


# 3.사용자 정보 조회 - 1.내 정보 조회
@router.get("/info", status_code=200, response_model=schemas.User)
async def my_info(
    request: Request, db: Session = Depends(get_db), _: str = Depends(auth_scheme)
):
    db_user = crud.get_user(db, email=request.state.email)
    return db_user

