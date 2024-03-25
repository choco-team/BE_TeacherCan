from teachercan.students.models import Allergy, Row, Student
from teachercan.columns.models import Column
from . import schemas
from .models import StudentList
from ..auths.api import AuthBearer
from ninja import Router
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import config.exceptions as ex

router = Router(auth=AuthBearer(), tags=["StudentList"])


@router.get("", response=schemas.GetStudentList)
def get_student_list(request):
    """
    모든 명렬표 보기(학생은 안보임)\n
    로그인만 하면 별도의 파라미터 없음
    """
    return {"studentList": StudentList.objects.filter(user=request.auth)}


@router.get("/{list_id}", response=schemas.StudentList)
def get_student_list_by_id(request, list_id: int):
    """
    특정 명렬표 보기(학생까지 보임)\n
    파라미터 값은 명렬표 id
    """
    try:
        student_list = StudentList.objects.get(id=list_id, user=request.auth)
    except ObjectDoesNotExist:
        raise ex.not_found_student_list
    return student_list


@router.post("", response=schemas.StudentList)
def post_student_list(
    request,
    payload: schemas.PostStudentListReq,
):
    """
    {\n
        "name": "3-2반 명렬표",
        "description": "우리반 명렬표",
        "students": [
            {
                "StudentNumber": 1,
                "StudentName": "김철수",
                "gender": "남"
            },
            {
                "StudentNumber": 2,
                "StudentName": "김영희",
                "gender": "여"
            }
        ]
    }
    """
    user = request.auth
    new_student_list = StudentList(
        name=payload.name,
        description=payload.description,
        has_allergy=False,
        is_main=not user.studentLists.count(),
        user=user,
    )
    students = [
        Student(
            number=s.number, name=s.name, gender=s.gender, student_list=new_student_list
        )
        for s in payload.students
    ]
    with transaction.atomic():
        new_student_list.save()
        for s in students:
            s.save()
    return new_student_list


@router.put("/main/")
def put_student_list_main(request, payload: schemas.PutMainReq):
    user = request.auth
    try:
        student_list = StudentList.objects.get(id=payload.id, user=user)
    except ObjectDoesNotExist:
        raise ex.not_found_student_list

    # is_main == false 를 true로 바꿀 때
    if not student_list.is_main and payload.is_main:
        try:
            main_student_list = StudentList.objects.get(user=user, is_main=True)
        except ObjectDoesNotExist:
            raise ex.not_found_student_list
        main_student_list.is_main = False
        student_list.is_main = payload.is_main
        main_student_list.save()
        student_list.save()
    # is_main == true 를 false로 바꿀 때
    elif student_list.is_main and not payload.is_main:
        try:
            recent_student_list = StudentList.objects.filter(
                user=user, is_main=False
            ).order_by("-updated_at")[0]
        except ObjectDoesNotExist:
            raise ex.not_found_student_list
        recent_student_list.is_main = True
        student_list.is_main = payload.is_main
        recent_student_list.save()
        student_list.save()
    return {"message": "성공적으로 변경 되었습니다."}


@router.delete("/{list_id}")
def delete_student_list(request, list_id: int):
    """
    명렬표 지우기(학생까지 다 지워짐)\n
    파라미터 값은 명렬표 id
    """
    try:
        student_list = StudentList.objects.get(id=list_id, user=request.auth)
    except ObjectDoesNotExist:
        raise ex.not_found_student_list
    if student_list.is_main == True:
        try:
            recent_student_list = StudentList.objects.filter(
                user=request.auth, is_main=False
            ).order_by("-updated_at")[0]
        except ObjectDoesNotExist:
            raise ex.not_found_student_list
        recent_student_list.is_main = True
        recent_student_list.save()
    student_list.delete()
    return {"message": "성공적으로 삭제 되었어요."}


@router.put("", response=schemas.StudentList)
def put_student_list(request, payload: schemas.PutStudentListReq):
    user = request.auth
    try:
        student_list = StudentList.objects.get(id=payload.id, user=user)
    except ObjectDoesNotExist:
        raise ex.not_found_student_list

    with transaction.atomic():
        student_list.name = payload.name
        student_list.description = payload.description
        # is_main == false 를 true로 바꿀 때
        if not student_list.is_main and payload.is_main:
            try:
                main_student_list = StudentList.objects.get(user=user, is_main=True)
            except ObjectDoesNotExist:
                raise ex.not_found_student_list
            main_student_list.is_main = False
            student_list.is_main = payload.is_main
            main_student_list.save()
        # is_main == true 를 false로 바꿀 때
        elif student_list.is_main and not payload.is_main:
            try:
                recent_student_list = StudentList.objects.filter(
                    user=user, is_main=False
                ).order_by("-updated_at")[0]
            except ObjectDoesNotExist:
                raise ex.not_found_student_list
            recent_student_list.is_main = True
            student_list.is_main = payload.is_main
            recent_student_list.save()
        student_list.has_allergy = student_list.has_allergy
        student_list.save()
        for column in payload.columns:
            try:
                col = Column.objects.get(id=column.id, student_list=student_list)
            except ObjectDoesNotExist:
                raise ex.not_found_column
            col.field = column.field
            col.save()
        for student in payload.students:
            try:
                s = Student.objects.get(id=student.id, student_list=student_list)
            except ObjectDoesNotExist:
                raise ex.not_found_student
            s.number = student.number
            s.name = student.name
            s.gender = student.gender
            if student_list.has_allergy and student.allergy:
                s.allergy.set([Allergy.objects.get(pk=a) for a in student.allergy])
            for row in student.rows:
                try:
                    r = Row.objects.get(column=col, student=s)
                    r.value = row.value
                    r.save()
                except ObjectDoesNotExist:
                    raise ex.not_found_row
            s.save()
    return student_list
