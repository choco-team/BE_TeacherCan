from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import decode

from .database import SessionLocal
from .errors import exceptions as ex
from .common.consts import JWT_ALGORITHM, JWT_SECRET


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
