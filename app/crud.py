from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import environ
import requests


from . import models, schemas


# env init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))


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
NICE_URL = "https://open.neis.go.kr/hub"


def search_schools(
    name: str | None = None, page_number: int | None = 1, data_size: int | None = 10
) -> list[schemas.SchoolList]:
    params = {
        "Type": "json",
        "KEY": env("NICE_API_KEY"),
        "SCHUL_NM": name,
        "pindex": page_number,
        "pSize": data_size,
    }

    try:
        response = requests.get(f"{NICE_URL}/schoolInfo", params=params).json()[
            "schoolInfo"
        ]
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        if (
            code == 200 or code == 336
        ):  # 200: 해당하는 데이터가 없습니다. / 336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다
            raise HTTPException(
                status_code=400,
                detail={"code": 400, "message": response["RESULT"]["MESSAGE"]},
            )
        else:
            raise HTTPException(
                status_code=500, detail={"code": 500, "message": "내부 API호출 실패"}
            )
    schools = [schemas.SchoolList(**school) for school in response[1]["row"]]
    total_page = (response[0]["head"][0]["list_total_count"] // data_size) + 1

    return schemas.SchoolLists(
        schoollist=schools,
        pagination=schemas.Pagination(
            pageNumber=page_number, dataSize=data_size, totalPageNumber=total_page
        ),
    )


def get_school(db: Session, code: str | None = None):
    result = db.query(models.School).filter(models.School.code == code).first()
    print(result)
    return result
