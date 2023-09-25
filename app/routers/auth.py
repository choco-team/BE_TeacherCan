from datetime import datetime, timedelta

from django.contrib.auth.hashers import check_password

from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session

from jwt import encode

from .. import crud, schemas
from ..schemas import ResponseModel, ResponseWrapper
from ..dependencies import get_db
from ..errors import exceptions as ex

from ..common.consts import JWT_ALGORITHM, JWT_SECRET

router = APIRouter(prefix="/auth", tags=["Auth"])


# Auth
# 1.이메일 중복검사
@router.post(
    "/signup/validation",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.Result],
)
def is_email_usable(user: schemas.UserBase, db: Session = Depends(get_db)):
    """
    `이메일 중복검사`
    """
    db_user = crud.get_user(db, email=user.email, not_found_error=False)
    if db_user:
        raise ex.EmailAlreadyExist()
    return ResponseWrapper({"result": True, "message": "이 이메일은 사용할 수 있어요."})


# 2.회원가입
@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[schemas.Result],
)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    `회원가입`
    """
    crud.create_user(db, user=user)
    return ResponseWrapper({"result": True, "message": "회원가입이 완료되었어요."})


# 3.로그인
@router.post("/signin", status_code=200, response_model=ResponseModel[schemas.Token])
def signin(user: schemas.UserSignin, db: Session = Depends(get_db)):
    """
    `로그인`
    """
    db_user = crud.get_user(db, email=user.email, not_found_error=True)
    if not check_password(user.password, db_user.password):
        raise ex.PasswordNotMatch()

    # Edit last_login
    setattr(db_user, "last_login", datetime.utcnow())
    db.commit()
    db.refresh(db_user)

    # Create jwt
    token = encode(
        {"email": user.email, "exp": datetime.utcnow() + timedelta(hours=24)},
        JWT_SECRET,
        JWT_ALGORITHM,
    )

    return ResponseWrapper({"result": True, "message": "Success Login", "token": token})
