from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from . import models, schemas


# User
def get_user(db: Session, email: str = None):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


def create_user(db: Session, user: schemas.UserCreate):
    if get_user(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already Exists."
        )

    # password validation
    try:
        validate_password(user.password)
    except ValidationError as error:
        message = ""
        for error_message in error.messages:
            message = f"{message} {error_message}"
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["body", "password"],
                    "msg": message.lstrip(),
                    "type": "value_error.password",
                }
            ],
        )

    hashed_password = make_password(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        nickname=user.nickname,
        joined_at=datetime.utcnow(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def update_user(db: Session, email: str, user: schemas.UserUpdate):
    db_user = get_user(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Token."
        )
    print("Running update_user!! school_code =", user.school_id)
    for field, value in user.dict().items():
        setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user


# School
def get_school(db: Session, code: str):
    result = db.query(models.School).filter(models.School.code == code).first()
    print(result)
    return result
