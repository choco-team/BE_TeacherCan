from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import requests


from . import models, schemas
from .common.consts import NICE_URL, NICE_API_KEY


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

    if user.school_id:
        db_school = get_school(db, code=user.school_id)
        if not db_school:
            create_school(db=db, code=user.school_id)

    for field, value in user.model_dump().items():
        setattr(db_user, field, value)
    setattr(db_user, "school_id", user.school_id)
    db.commit()
    db.refresh(db_user)
    return db_user


def api_search_schools(
    name: str | None = None,
    code: str | None = None,
    page_number: int | None = 1,
    data_size: int | None = 10,
) -> schemas.SchoolLists:
    params = {
        "Type": "json",
        "KEY": NICE_API_KEY,
        "SD_SCHUL_CODE": code,
        "SCHUL_NM": name,
        "pindex": page_number,
        "pSize": data_size,
    }
    try:
        response = requests.get(f"{NICE_URL}/schoolInfo", params=params).json()
    except:
        raise HTTPException(status_code=500, detail="교육정보포털 api 에러")

    try:
        school_info = response["schoolInfo"]
        total = int(school_info[0]["head"][0]["list_total_count"])
        schools = [schemas.SchoolList(**school) for school in school_info[1]["row"]]
        return schemas.SchoolLists(
            **{
                "schoollist": schools,
                "pagination": {
                    "pageNumber": page_number,
                    "dataSize": data_size,
                    "totalPageNumber": -(-total // data_size),
                },
            }
        )
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        # 200: 해당하는 데이터가 없습니다. / 336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다
        if code == 200:
            raise HTTPException(status_code=404, detail="해당하는 학교가 없습니다.")
        elif code == 336:
            raise HTTPException(
                status_code=400,
                detail={"code": 400, "message": response["RESULT"]["MESSAGE"]},
            )
        else:
            raise HTTPException(
                status_code=500, detail={"code": 500, "message": "내부 API호출 실패"}
            )


def get_school(db: Session, code: str | None = None):
    result = db.query(models.School).filter(models.School.code == code).first()
    print(result)
    return result


def create_school(db: Session, code: str):
    school = api_search_schools(code=code).schoollist[0]
    db_school = models.School(
        code=code, name=school.schoolName, area_code=school.areaCode
    )
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
