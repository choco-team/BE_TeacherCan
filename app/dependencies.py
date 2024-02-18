from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode


from .database import SessionLocal
from .errors import exceptions as ex
from .common.consts import JWT_ALGORITHM, JWT_SECRET

from teachercan.users.models import User

from sqlalchemy.orm import Session
from app import models


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 토큰 검증
def verify_token(
    token: HTTPAuthorizationCredentials = Depends(
        HTTPBearer(scheme_name="token", auto_error=False)
    )
):
    if not (token and (token.scheme == "Bearer") and token.credentials):
        raise ex.NotAuthenticated()
    try:
        payload = decode(token.credentials, JWT_SECRET, JWT_ALGORITHM)
    except:
        raise ex.InvalidToken()
    return payload


# token payload에서 email 반환
def user_email(payload=Depends(verify_token)) -> str:
    email = payload.get("email")
    if not email:
        raise ex.InvalidToken()
    return email


# token payload에서 user 반환
def user(payload=Depends(verify_token)) -> User:
    email = payload.get("email")
    user = User.objects.get(email=email)
    if not user:
        raise ex.InvalidToken()
    return user

def user(payload=Depends(verify_token)) -> User:
    email = payload.get("email")
    user = User.objects.get(email=email)
    if not user:
        raise ex.InvalidToken()
    return user

def get_db_user(payload=Depends(verify_token), db: Session = Depends(get_db)) -> User:
    email = payload.get("email")
    user = db.query(models.User).filter(models.User.email == email)
    return (db, user)

def get_verified_db(payload=Depends(verify_token), db: Session = Depends(get_db)) -> Session:
    return db