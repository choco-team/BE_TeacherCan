from sqlalchemy.orm import Session
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from app.errors import exceptions as ex

from app import models

from app.crud import school_crud
from app.schemas import user_schemas

# User
def get_user(
    db: Session, email: str = None, not_found_error: bool = True
) -> models.User | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not_found_error and not user:
        raise ex.NotFoundUser()
    return user

def get_user_signin(
    db: Session, email: str = None, not_found_error: bool = True
) -> models.User | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not_found_error and not user:
        raise ex.SigninNotMatch()
    return user


def create_user(db: Session, user: user_schemas.UserCreate):
    if get_user(db, email=user.email, not_found_error=False):
        raise ex.EmailAlreadyExist()

    # password validation
    try:
        validate_password(user.password)
    except ValidationError as error:
        raise ex.PasswordInvalid(data=error.messages)

    hashed_password = make_password(user.password)
    db_user = models.User(
        email=user.email,
        password=hashed_password,
        nickname=user.nickname,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def update_user(db: Session, email: str, user: user_schemas.UserUpdate):
    db_user = get_user(db, email=email)

    if user.school_id:
        db_school = school_crud.get_school(db, code=user.school_id)
        if not db_school:
            school_crud.create_school(db=db, code=user.school_id)

    for field, value in user.model_dump().items():
        setattr(db_user, field, value)
    setattr(db_user, "school_id", user.school_id)
    db.commit()
    db.refresh(db_user)
    return db_user