from teachercan.students.models import Allergy, Row, Student
from teachercan.student_lists.models import StudentList
from .models import Column
from . import schemas
from ..auths.api import AuthBearer
from ninja import Router
from django.db import transaction
import config.exceptions as ex


router = Router(auth=AuthBearer(), tags=["Column"])


@router.get('/list/{studentListId}', response=schemas.GetColumnRes)
def get_colomn_list_router(request, studentListId: int):
    try:
        StudentList.objects.get(id=studentListId, user=request.auth)
    except:
        raise ex.not_access_permission
    columns = Column.objects.filter(student_list_id=studentListId)
    return {"columns": columns}


@router.post('')
def post_column_router(request, payload: schemas.PostColumnReq):
    try:
        student_list = StudentList.objects.get(id = payload.student_list_id)
    except:
        raise ex.not_found_student_list
    try:
        students = Student.objects.filter(student_list=student_list)
    except:
        raise ex.not_found_student
    new_column = Column(
        field = payload.field,
        student_list=student_list
    )
    rows = [
        Row(
            student=s,
            column=new_column
        )
        for s in students
    ]
    with transaction.atomic():
        new_column.save()
        for s in rows:
            s.save()
    return "column이 성공적으로 저장되었습니다."


@router.put('', response=schemas.ColumnWithId)
def put_column_router(request, payload: schemas.ColumnWithId):
    try:
        column = Column.objects.get(id=payload.id)
    except:
        raise ex.not_found_column
    if not column.student_list.user == request.auth:
        raise ex.not_access_permission

    with transaction.atomic():
        column.field = payload.field
        column.save()
    return column


@router.delete('')
def delete_column_router(request, column_id: int):
    try:
        column = Column.objects.get(id=column_id)
    except:
        raise ex.not_found_column
    if not column.student_list.user == request.auth:
        raise ex.not_access_permission
    column.delete()
    return "column을 성공적으로 삭제했습니다."