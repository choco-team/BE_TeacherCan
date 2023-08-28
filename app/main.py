from django.conf import settings

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
import jwt

from . import models
from .database import engine
from .routers import auth, user, school
from .common.consts import DJANGO_SECRET_KEY, JWT_ALGORITHM, JWT_SECRET, ALLOWED_HOSTS

# django auth 사용을 위한 config
settings.configure(
    SECRET_KEY=DJANGO_SECRET_KEY,
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

app = FastAPI(root_path="/api")


# middleware
# 토큰 검증
@app.middleware("http")
async def check_access(request: Request, call_next):
    path = request.url.path
    except_path_list = [
        "/api/",
        "/api/docs",
        "/api/redoc",
        "/api/openapi.json",
        "/api/auth/signup/validation",
        "/api/auth/signup",
        "/api/auth/signin",
        "/api/school/list",
    ]
    key = request.headers.get("Authorization")
    print(path)
    if path in except_path_list:
        ...
    elif key:
        key = key.replace("Bearer ", "")
        try:
            request.state.email = jwt.decode(key, JWT_SECRET, JWT_ALGORITHM)["email"]
        except:
            return JSONResponse(status_code=401, content={"message": "토큰 검증에 실패했습니다."})

    else:
        return JSONResponse(status_code=401, content={"message": "토큰 검증에 실패했습니다."})
    response = await call_next(request)
    return response


# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# TrustedHost 미들웨어
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)

# router
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(school.router)


@app.get("/")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}
