from django.conf import settings

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import environ

import jwt

from . import models
from .database import engine
from .routers import school, user
from . import crud, schemas
from .dependencies import get_db

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

# middleware
# 토큰 검증
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
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost"])

# router
app.include_router(user.router)
app.include_router(school.router)


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


