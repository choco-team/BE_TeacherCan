from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.models import *
from app import models
from app.errors import exceptions as ex


from app.schemas import student_schemas
from app.crud import studentList_crud

def get_student(db: Session, studentListId:int):
    students = db.query(Student).filter(Student.list_id == studentListId).all()
    if not students:
        raise HTTPException(status_code=404, detail="학생이 존재하지 않아요.")    
    return students


def convert_student_allergy(student: student_schemas.Student):
    student.allergies = [allergy.code for allergy in student.allergy]
    return student

def convert_student_allergy(student: student_schemas.Student):
    student.allergies = [allergy.code for allergy in student.allergy]
    return student

def allergy(db: Session, codes: list[int]):
    stmt = select(models.Allergy).where(models.Allergy.code.in_(codes))
    db_allergy = db.scalars(stmt).all()
    return db_allergy

def get_student_by_email(db: Session, email: str, student_id: int):
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
    db: Session, email: str, list_id: int, student: student_schemas.StudentCreate
):
    db_student_list = studentList_crud.get_student_list(db, email, list_id)

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
    db: Session, email: str, student_id: int, student: student_schemas.StudentUpdate
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