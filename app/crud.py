from sqlalchemy.orm import Session
from django.contrib.auth.hashers import (
    make_password,
    check_password,
    is_password_usable,
)

from . import models, schemas


# User
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()


def create_user(db: Session, user_id: str, password: str, nickname: str):
    return make_password(password)


def get_school(db: Session, school_code: str):
    result = (
        db.query(models.School).filter(models.School.school_code == school_code).first()
    )
    print(result)
    return result


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# def create_user(db: Session, user: schemas.UserCreate):
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item


# def delete_user(db: Session, user_id: int):
#     print("/////////////////////////////////////")
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     db.query()
#     return db.query(models.User).filter(models.User.id == user_id).first()
