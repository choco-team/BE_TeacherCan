from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import (
    make_password,
    check_password,
    is_password_usable,
)
import environ
import jwt
from fastapi import Depends, FastAPI, HTTPException, APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# 환경변수 init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

# django auth 사용을 위한 config
settings.configure(
    SECRET_KEY=env("DJANGO_SECRET_KEY"),
    USE_I18N=False,
    AUTH_PASSWORD_VALIDATORS=[
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
        },
    ],
)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(prefix="/user", tags=["User"])


# User
# 1.회원가입 - 1.이메일 중복검사
@user_router.post(
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
@user_router.post(
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
        raise HTTPException(
            status_code=400, detail={"result": False, "message": "이미 가입된 이메일입니다."}
        )
    try:
        validate_password(user.password)
    except ValidationError as error:
        message = ""
        for error_message in error.messages:
            message = f"{message} {error_message}"
        raise HTTPException(
            status_code=422,
            detail={
                "detail": [
                    {
                        "loc": ["body", "password"],
                        "msg": message.lstrip(),
                        "type": "value_error.password",
                    }
                ]
            },
        )

    # print(
    #     crud.create_user(
    #         db, email=user.email, password=user.password, nickname=user.nickname
    #     )
    # )

    return {"result": True, "message": "회원가입이 완료되었습니다."}


# 1.회원가입 - 3.로그인
@user_router.post("/auth/signin", status_code=200, response_model=schemas.Token)
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


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


@app.get("/school/{school_code}", response_model=schemas.School)
def read_school(school_code: str, db: Session = Depends(get_db)):
    db_school = crud.get_school(db, school_code=school_code)

    password = "1234"
    hashed_password = make_password(password)
    print(check_password(password, hashed_password))
    print(db_school.users)
    return db_school


@app.get("/userinfo/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserSchool)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    print(db_user.school)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

# @app.delete("/users/{user_id}", response_model=schemas.User)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.delete_user(db, user_id=user_id)
#     return db_user

app.include_router(user_router)
