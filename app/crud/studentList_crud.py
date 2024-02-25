from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from app import models
from app.errors import exceptions as ex

from app.models import StudentList

def get_student_list_asd(db: Session, student_list_id:int):
    student_list = db.query(StudentList).get(student_list_id)
    if not student_list:
        raise HTTPException(status_code=404, detail="요청하신 명렬표가 존재하지 않아요.") 
    return student_list   



# Student
# def convert_student_allergy(student: schemas.Student):
#     student.allergies = [allergy.code for allergy in student.allergy]
#     return student

# def convert_students_allergy(students: list[schemas.Student]):
#     for student in students:
#         student = convert_student_allergy(student)
#     return students

# def create_student_list(
#     db: Session, email: str, student_list: schemas.StudentListCreate
# ):
#     db_user = get_user(db, email)
#     db_students = []
#     for student in student_list.students:
#         db_student = models.Student(
#             name=student.name,
#             number=student.number,
#             is_male=student.is_male,
#             description=student.description,
#             allergy=allergy(db, student.allergy),
#         )
#         db_students.append(db_student)
#     db_student_list = models.StudentList(
#         name=student_list.name,
#         user_id=db_user.id,
#         is_main=student_list.is_main,
#         students=db_students,
#     )
#     db.add(db_student_list)
#     db.commit()
#     db.refresh(db_student_list)
#     db_student_list.students = convert_students_allergy(db_student_list.students)
#     return db_student_list


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


# def get_student_lists(db: Session, email: str):
#     stmt = (
#         select(models.StudentList)
#         .join(models.User.student_list)
#         .where(models.User.email == email)
#     )
#     db_student_lists = db.scalars(stmt).all()
#     if db_student_lists:
#         for db_student_list in db_student_lists:
#             db_student_list.students = convert_students_allergy(
#                 db_student_list.students
#             )
#         return db_student_lists
#     raise ex.NotExistStudentList()


# def delete_student_list(db: Session, email: str, list_id: int):
#     db_student_list = get_student_list(db, email, list_id)
#     db.delete(db_student_list)
#     db.commit()


# def update_student_list(
#     db: Session, email: str, list_id: int, student_list: schemas.StudentListUpdate
# ):
#     db_student_list = get_student_list(db, email, list_id)
#     db_student_list.name = student_list.name
#     db_student_list.is_main = student_list.is_main
#     db.flush()
#     db.commit()
#     db.refresh(db_student_list)
#     db_student_list.students = convert_students_allergy(db_student_list.students)
#     return db_student_list