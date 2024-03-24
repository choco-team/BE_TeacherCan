from ninja import Schema, Field
from pydantic import EmailStr


class EmailIn(Schema):
    email: EmailStr


class SignUpIn(Schema):
    email: EmailStr
    password: str = Field(max_length=20)
    nickname: str = Field(max_length=50)


class SignInIn(Schema):
    email: EmailStr
    password: str
