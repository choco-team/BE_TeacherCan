from django.conf import settings

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

import environ

import jwt

from . import models
from .database import engine
from .routers import auth, user, school

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
        "/auth/signup/validation",
        "/auth/signup",
        "/auth/signin",
        "/school/list",
    ]
    key = request.headers.get("Authorization")
    if path in except_path_list:
        ...
    elif key:
        key = key.replace("Bearer ", "")
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
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(school.router)
