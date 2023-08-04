from datetime import datetime

from sqlalchemy.orm import Session
from django.contrib.auth.hashers import (
    make_password,
    check_password,
    is_password_usable,
)

from . import models, schemas


# User
def get_user(db: Session, email: str = None, nickname: str = None):
    if email and nickname:
        return (
            db.query(models.User)
            .filter(models.User.email == email, models.User.nickname == nickname)
            .first()
        )
    if email:
        return db.query(models.User).filter(models.User.email == email).first()
    return db.query(models.User).filter(models.User.nickname == nickname).first()


def create_user(db: Session, user: schemas.UserCreate):
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
    return db_user


def get_school(db: Session, code: str):
    result = db.query(models.School).filter(models.School.code == code).first()
    print(result)
    return result
