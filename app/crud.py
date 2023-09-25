from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import requests


from . import models, schemas
from .common.consts import NICE_URL, NICE_API_KEY
from .errors import exceptions as ex


# User
def get_user(
    db: Session, email: str = None, not_found_error: bool = True
) -> models.User | None:
    user = db.query(models.User).filter(models.User.email == email).first()
    if not_found_error and not user:
        raise ex.NotFoundUser()
    return user


def create_user(db: Session, user: schemas.UserCreate):
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


def update_user(db: Session, email: str, user: schemas.UserUpdate):
    db_user = get_user(db, email=email)

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


# School
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
        raise ex.NiceApiError()

    try:
        school_info = response["schoolInfo"]
        total = int(school_info[0]["head"][0]["list_total_count"])
        schools = [schemas.SchoolList(**school) for school in school_info[1]["row"]]
        return schemas.SchoolLists(
            **{
                "school_list": schools,
                "pagination": {
                    "page_number": page_number,
                    "data_size": data_size,
                    "total_page_number": -(-total // data_size),
                },
            }
        )
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        # 200: 해당하는 데이터가 없습니다. / 336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다
        if code == 200:
            raise ex.NotFoundSchool()
        elif code == 336:
            raise ex.TooLargeEntity()
        else:
            raise Exception()


def get_school(db: Session, code: str | None = None):
    result = db.query(models.School).filter(models.School.code == code).first()
    return result


def create_school(db: Session, code: str):
    school = api_search_schools(code=code).school_list[0]
    db_school = models.School(
        code=code, name=school.school_name, area_code=school.area_code
    )
    db.add(db_school)
    db.commit()
    db.refresh(db_school)


def allergy(db: Session, codes: list[int]):
    stmt = select(models.Allergy).where(models.Allergy.code.in_(codes))
    db_allergy = db.scalars(stmt).all()
    return db_allergy


# Student
def convert_student_allergy(student: schemas.Student):
    student.allergies = [allergy.code for allergy in student.allergy]
    return student


def convert_students_allergy(students: list[schemas.Student]):
    for student in students:
        student = convert_student_allergy(student)
    return students


def create_student_list(
    db: Session, email: str, student_list: schemas.StudentListCreate
):
    db_user = get_user(db, email)
    db_students = []
    for student in student_list.students:
        db_student = models.Student(
            name=student.name,
            number=student.number,
            is_male=student.is_male,
            description=student.description,
            allergy=allergy(db, student.allergy),
        )
        db_students.append(db_student)
    db_student_list = models.StudentList(
        name=student_list.name,
        user_id=db_user.id,
        is_main=student_list.is_main,
        students=db_students,
    )
    db.add(db_student_list)
    db.commit()
    db.refresh(db_student_list)
    db_student_list.students = convert_students_allergy(db_student_list.students)
    return db_student_list


def get_student_list(db: Session, email: str, list_id: int):
    stmt = (
        select(models.StudentList)
        .join(models.User.student_list)
        .where(models.User.email == email)
        .where(models.StudentList.id == list_id)
    )
    try:
        db_student_list = db.scalars(stmt).one()
        db_student_list.students = convert_students_allergy(db_student_list.students)
        return db_student_list
    except NoResultFound:
        raise ex.NotFoundStudentList()


def get_student_lists(db: Session, email: str):
    stmt = (
        select(models.StudentList)
        .join(models.User.student_list)
        .where(models.User.email == email)
    )
    db_student_lists = db.scalars(stmt).all()
    if db_student_lists:
        for db_student_list in db_student_lists:
            db_student_list.students = convert_students_allergy(
                db_student_list.students
            )
        return db_student_lists
    raise ex.NotExistStudentList()


def delete_student_list(db: Session, email: str, list_id: int):
    db_student_list = get_student_list(db, email, list_id)
    db.delete(db_student_list)
    db.commit()


def update_student_list(
    db: Session, email: str, list_id: int, student_list: schemas.StudentListUpdate
):
    db_student_list = get_student_list(db, email, list_id)
    db_student_list.name = student_list.name
    db_student_list.is_main = student_list.is_main
    db.flush()
    db.commit()
    db.refresh(db_student_list)
    db_student_list.students = convert_students_allergy(db_student_list.students)
    return db_student_list


def get_student(db: Session, email: str, student_id: int):
    stmt = (
        select(models.Student)
        .join(models.StudentList)
        .join(models.User)
        .where(models.User.email == email)
        .where(models.Student.id == student_id)
    )
    try:
        db_student = db.scalars(stmt).one()
        return convert_student_allergy(db_student)
    except NoResultFound:
        raise ex.NotFoundStudent()


def create_student(
    db: Session, email: str, list_id: int, student: schemas.StudentCreate
):
    db_student_list = get_student_list(db, email, list_id)

    db_student = models.Student(
        list_id=list_id,
        name=student.name,
        number=student.number,
        is_male=student.is_male,
        description=student.description,
        allergy=allergy(db, student.allergy),
    )

    db_student_list.students.append(db_student)
    db.commit()
    db.refresh(db_student)
    return convert_student_allergy(db_student)


def update_student(
    db: Session, email: str, student_id: int, student: schemas.StudentUpdate
):
    db_student = get_student(db, email, student_id)
    db_student.name = student.name
    db_student.number = student.number
    db_student.is_male = student.is_male
    db_student.description = student.description
    db_student.allergy = allergy(db, student.allergy)

    db.flush()
    db.commit()
    db.refresh(db_student)
    return convert_student_allergy(db_student)


def delete_student(db: Session, email: str, student_id: int):
    db_student = get_student(db, email, student_id)
    db.delete(db_student)
    db.commit()
