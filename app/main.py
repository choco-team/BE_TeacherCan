from typing import Annotated
from datetime import datetime, timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import (
    make_password,
    check_password,
    is_password_usable,
)

from fastapi import Query, Depends, FastAPI, HTTPException, APIRouter, status, Request, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

import environ
import jwt
import requests
import math

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


# Router
user_router = APIRouter(prefix="/user", tags=["User"])
school_router = APIRouter(prefix="/school", tags=["School"])


# swagger ui 헤더에 jwt 추가를 위한 스키마
auth_scheme = HTTPBearer()


# middleware
# 토큰 검증 미들웨어
@app.middleware("http")
async def check_access(request: Request, call_next):
    path = request.url.path
    except_path_list = [
        "/",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/user/auth/signup/validation",
        "/user/auth/signup",
        "/user/auth/signin",
        "/school/list",
        "/school/lunch-menu"
    ]
    key = request.headers.get("Authorization")
    print(key)
    if path in except_path_list:
        ...
    elif key:
        key = key.replace("Bearer ", "")
        print(jwt.decode(key, env("JWT_SECRET"), env("JWT_ALGORITHM")))
        request.state.email = jwt.decode(key, env("JWT_SECRET"), env("JWT_ALGORITHM"))[
            "email"
        ]
    else:
        return JSONResponse(status_code=400, content={"message": "토큰 검증에 실패했습니다."})

    response = await call_next(request)
    return response


# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TrustedHost 미들웨어
app.add_middleware(TrustedHostMiddleware, allowed_hosts=[
                   "127.0.0.1", "localhost"])


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


# 3.사용자 정보 조회 - 1.내 정보 조회
@user_router.get("/info", status_code=200, response_model=schemas.User)
async def my_info(
    request: Request, db: Session = Depends(get_db), _: str = Depends(auth_scheme)
):
    db_user = crud.get_user(db, email=request.state.email)
    return db_user


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)

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


# school
niceKEY = env("NICE_API_KEY")
niceURL = "https://open.neis.go.kr/hub"
params = {"Type": "json", "KEY": niceKEY}
# 1. 학교정보 - 1. 학교 정보 검색


def filterSchoolList(school):
    return {
        "schoolName": school["SCHUL_NM"],
        "schoolAddress": school["ORG_RDNMA"],
        "schoolCode": school["SD_SCHUL_CODE"],
        "areaCode": school["ATPT_OFCDC_SC_CODE"]
    }


@school_router.get("/list", status_code=200, response_model=schemas.SchoolLists)
# schoolName = None : 모든 학교를 ㄱㄴㄷ 순으로 응답
async def schoolList(schoolName: str | None = None, pageNumber: int | None = 1, dataSize: int | None = 10):
    nParams = params.copy()
    nParams.update(
        {"SCHUL_NM": schoolName, "pIndex": pageNumber, "pSize": dataSize})
    response = requests.get(f"{niceURL}/schoolInfo", params=nParams).json()
    try:
        response["schoolInfo"]
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        if code == 200 or code == 336:  # 200: 해당하는 데이터가 없습니다. / 336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다
            raise HTTPException(status_code=400, detail={
                                "code": 400, "message": response["RESULT"]["MESSAGE"]})
        else:
            raise HTTPException(status_code=500, detail={
                                "code": 500, "message": "내부 API호출 실패"})
    schoolList = list(map(filterSchoolList, response["schoolInfo"][1]["row"]))
    totalPageNumber = math.ceil(
        response["schoolInfo"][0]["head"][0]["list_total_count"]/dataSize)
    return JSONResponse(status_code=200, content={
        "schoolList": schoolList,
        "pagination": {
            "pageNumber": pageNumber,
            "dataSize": dataSize,
            "totalPageNumber": totalPageNumber,
        }
    }
    )


# 2. 급식정보 - 1. 급식 정보 조회
def lunchMenuToDict(str):
    splited = str.split(" ")
    return {"menu": splited[0], "allergy": [] if not splited[1] else list(map(int, splited[1].strip("("")").split(".")))}


def originToDict(str):
    splited = str.split(" : ")
    return {"ingredient": splited[0], "origin": splited[1]}


@school_router.get("/lunch-menu", status_code=200, response_model=schemas.SchoolLunch)
async def schoolLunch(areaCode: str | None, schoolCode: int | None, date: Annotated[int | None, Query(ge=10000000, lt=100000000)]):
    nParams = params.copy()
    nParams.update(
        {"ATPT_OFCDC_SC_CODE": areaCode, "SD_SCHUL_CODE": schoolCode, "MLSV_YMD": date})
    response = requests.get(
        f"{niceURL}/mealServiceDietInfo", params=nParams).json()
    try:
        response["mealServiceDietInfo"]
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        if code == 200:  # 200: 해당하는 데이터가 없습니다.
            raise HTTPException(status_code=400, detail={
                                "code": 400, "message": response["RESULT"]["MESSAGE"]})
        else:
            raise HTTPException(status_code=500, detail={
                                "code": 500, "message": "내부 API호출 실패"})
    row = response["mealServiceDietInfo"][1]["row"][0]
    lunchMenu = list(map(lunchMenuToDict, row["DDISH_NM"].split("<br/>")))
    origin = list(map(originToDict, row["ORPLC_INFO"].split("<br/>")))
    return JSONResponse(status_code=200, content={
        "lunchMenu": lunchMenu,
        "origin": origin
    })


# 뭔지 모르겠지만 school_router로 가져왔습니다.


@school_router.get("/{school_code}", response_model=schemas.School)
def read_school(school_code: str, db: Session = Depends(get_db)):
    db_school = crud.get_school(db, school_code=school_code)
    password = "1234"
    hashed_password = make_password(password)
    print(check_password(password, hashed_password))
    print(db_school.users)
    return db_school


app.include_router(user_router)
app.include_router(school_router)
