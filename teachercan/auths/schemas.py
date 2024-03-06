from ninja import Schema
from pydantic import EmailStr


class EmailIn(Schema):
    email: EmailStr


class SignUpIn(Schema):
    email: EmailStr
    password: str
    nickname: str


class SignInIn(Schema):
    email: EmailStr
    password: str
