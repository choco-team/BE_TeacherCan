from datetime import datetime, timedelta

from ninja import Router
from ninja.security import HttpBearer
from django.contrib.auth import authenticate, login
from jwt import encode, decode


from config.settings import JWT_ALGORITHM, JWT_SECRET
from teachercan.users.models import User
from teachercan.auths import schemas
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
@router.post("/signup/validation")
def is_email_usable(request, payload: schemas.EmailIn):
    """
    `이메일 중복검사`
    """
    user_count = User.objects.filter(email=payload.email).count()
    if user_count:
        raise ex.email_already_exist
    # if User.objects.has_user(payload.email):
    #     raise ex.email_already_exist
    return "사용 가능한 이메일입니다."


# 2.회원가입
@router.post("/signup")
def signup(request, user: schemas.SignUpIn):
    """
    `회원가입`
    """
    User.objects.create_user(
        email=user.email, password=user.password, nickname=user.nickname
    )
    return "회원가입이 완료되었어요."


# 3.로그인
@router.post("/signin")
def signin(request, user: schemas.SignInIn):
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
        return {"token" : token}

    return "로그인 실패"
