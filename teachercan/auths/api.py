from datetime import datetime, timedelta

from ninja import Router
from ninja.security import HttpBearer
from django.contrib.auth import authenticate, login
from jwt import encode, decode


from config.settings import JWT_ALGORITHM, JWT_SECRET
from teachercan.users.models import User
from .schemas import EmailIn, SignUpIn, SignInIn
import config.exceptions as ex


class AuthBearer(HttpBearer):
    def authenticate(self, request, token=""):
        try:
            payload = decode(token, JWT_SECRET, JWT_ALGORITHM)
            user = User.objects.get(email=payload["email"])
            login(request, user)
        except:
            raise ex.invalid_token
        return user


router = Router(tags=["Auth"])


# 1.이메일 중복검사
@router.post("/signup/validation", response={201: dict, 409: dict})
def is_email_usable(request, payload: EmailIn):
    """
    `이메일 중복검사`
    """
    if User.objects.has_user(payload.email):
        raise ex.email_already_exist
    return 201, {"code": 2000, "message": "이 이메일은 사용할 수 있어요."}


# 2.회원가입
@router.post("/signup", response={201: dict})
def signup(request, user: SignUpIn):
    """
    `회원가입`
    """
    User.objects.create_user(
        email=user.email, password=user.password, nickname=user.nickname
    )
    return 201, {"code": 2000, "message": "회원가입이 완료되었어요."}


# 3.로그인
@router.post("/signin", response={200: dict, 401: dict})
def signin(request, user: SignInIn):
    """
    `로그인`
    """
    user = authenticate(email=user.email, password=user.password)
    if user:
        login(request, user)

        # Create jwt
        token = encode(
            {"email": user.email, "exp": datetime.utcnow() + timedelta(hours=24)},
            JWT_SECRET,
            JWT_ALGORITHM,
        )
        return 200, {"code": 2000, "token": token}

    return 401, {"code": 1104, "message": "로그인 실패"}
