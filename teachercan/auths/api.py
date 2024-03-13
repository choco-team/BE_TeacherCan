from datetime import datetime, timedelta

from ninja import Router
from ninja.security import HttpBearer
from django.contrib.auth import authenticate, login
from jwt import encode, decode
from config import exceptions as ex

from config.settings import JWT_ALGORITHM, JWT_SECRET
from teachercan.users.models import User
from .schemas import EmailIn, SignUpIn, SignInIn


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = decode(token, JWT_SECRET, JWT_ALGORITHM)
            user = User.objects.get(email=payload["email"])
            login(request, user)
        except:
            raise ValueError("토큰 인증 실패")
        return user


router = Router(tags=["Auth"])

from ninja import Schema
from pydantic import EmailStr

class Asd(Schema):
    email: EmailStr
    social_id: str

# 1.이메일 중복검사
@router.post("/signup/validation")
def is_email_usable(request, email: EmailIn):
    """
    `이메일 중복검사`
    """
    user_count = User.objects.filter(email=email.email).count()
    user = User.objects.get(id=1)
    if user_count:
        raise ex.EmailAlreadyExist()
    return "사용 가능한 아이디입니다."



# 2.회원가입
@router.post("/signup")
def signup(request, user: SignUpIn):
    """
    `회원가입`
    """
    User.objects.create_user(
        email=user.email, password=user.password, nickname=user.nickname
    )
    return {"result": True, "message": "회원가입이 완료되었어요."}


# 3.로그인
@router.post("/signin")
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
        return token

    return "로그인 실패"
