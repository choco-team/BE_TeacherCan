from fastapi import Depends, APIRouter, status, Query, Body
from sqlalchemy.orm import Session
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.core import serializers

from teachercan.users.models import StudentList, Student, User, Column, Allergy, Row

from app.routers.common_schemas import *
from app.dependencies import get_db, user_email, user
from app.errors import exceptions as ex

from app.schemas import studentList_schemas

router = APIRouter(prefix="/student/list", tags=["StudentList"])


# 명렬표
@router.get(
    "/", status_code=200, response_model=ResponseModel[studentList_schemas.GetStudentList]
)
def student_list(user: User = Depends(user)):
    """
    모든 명렬표 보기(학생은 안보임)\n
    로그인만 하면 별도의 파라미터 없음
    """
    return ResponseWrapper(
        studentList_schemas.GetStudentList(StudentList=StudentList.objects.filter(user=user))
    )


@router.get(
    "/{list_id}",
    status_code=200,
    response_model=ResponseModel[studentList_schemas.StudentListWithStudent],
)
def student_list(list_id: int, user: str = Depends(user)):
    """
    특정 명렬표 보기(학생까지 보임)\n
    파라미터 값은 명렬표 id
    """
    try:
        q = StudentList.objects.get(id=list_id, user=user)
    # 명렬표 없을 때 예외 처리
    except ObjectDoesNotExist:
        raise ex.NotExistStudentList()
    columns = [
        studentList_schemas.Column(id=column.id, field=column.field)
        for column in q.column_set.all()
    ]
    students = [
        studentList_schemas.StudentWithRows(
            id=e.id,
            number=e.number,
            name=e.name,
            gender=e.gender,
            allergy=[a.code for a in e.allergy.all()] if q.has_allergy else None,
            rows=[{"id": r.column.id, "value": r.value} for r in e.row_set.all()],
        )
        for e in q.student_set.all()
    ]
    return ResponseWrapper(
        studentList_schemas.StudentListWithStudent(
            id=q.id,
            name=q.name,
            is_main=q.is_main,
            has_allergy=q.has_allergy,
            created_at=q.created_at,
            updated_at=q.updated_at,
            columns=columns,
            students=students,
        )
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[studentList_schemas.StudentListWithStudent],
)
def student_list(
    student_list: studentList_schemas.StudentListCreate,
    user: str = Depends(user),
):
    """
    {\n
        "name": "3-2반 명렬표", // 명렬표 이름
        "isMain": false, // 메인 명렬표 여부
        "description": "우리반 명렬표", // 명렬표 설명
        "hasAllergy": false, // 알러지 정보 사용 여부
        "students": [ // 학생 정보 입력
            {
                "number": 1, // 번호
                "name": "김개똥", // 학생 이름
                "isMale": true, // 성별(true: 남자, false: 여자)
                "description": "맨 앞자리", // 학생 설명
                "allergy": [] // 알러지 정보, 없으면 빈 배열
            },
            {
                "number": 2, // 번호
                "name": "나승범", // 학생 이름
                "isMale": false, // 성별(true: 남자, false: 여자)
                "description": "급식 1번", // 학생 설명
                "allergy": [1, 2, 3] // 알러지 정보, 없으면 빈 배열
            },
        ]
    }
    """
    new_student_list = StudentList(
        name=student_list.name,
        has_allergy=student_list.has_allergy,
        is_main=not user.studentlist_set.count(),
        user=user,
    )
    students = [
        Student(
            number=s.number, name=s.name, gender=s.gender, student_list=new_student_list
        )
        for s in student_list.students
    ]
    # db 트랜잭션
    with transaction.atomic():
        new_student_list.save()
        for s in students:
            s.save()

    new_student_list.students = [
        studentList_schemas.StudentWithRows(
            id=s.id,
            number=s.number,
            name=s.name,
            gender=s.gender,
            allergy=[] if student_list.has_allergy else None,
            rows=[],
        )
        for s in students
    ]

    new_student_list.columns = []
    return ResponseWrapper(new_student_list)


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def student_list(
    list_id: int,
    user: str = Depends(user),
):
    """
    명렬표 지우기(학생까지 다 지워짐)\n
    파라미터 값은 명렬표 id
    """
    try:
        student_list = StudentList.objects.get(id=list_id, user=user)
    except ObjectDoesNotExist:
        raise ex.NotFoundStudentList()
    student_list.delete()
    return ResponseWrapper(data=None)

@router.put(
    "/main",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[str],
)
def put_student_list_main(
    update_main: studentList_schemas.UpdateMain,
    user: str = Depends(user)
):
    try:
        updated_student_list = StudentList.objects.get(id=update_main.id, user=user)
        tmp = StudentList.objects.get(user=user, is_main=True)
    except ObjectDoesNotExist:
        raise ex.NotExistStudentList()  
    
    tmp.is_main = False
    updated_student_list.is_main = update_main.isMain
    tmp.save()
    updated_student_list.save()

    return ResponseWrapper("성공적으로 변경 되었습니다.")

    

@router.put(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[studentList_schemas.StudentListWithStudent],
)
def student_list(
    student_list: studentList_schemas.StudentListUpdate,
    user: str = Depends(user),
):
    try:
        updated_student_list = StudentList.objects.get(id=student_list.id, user=user)
    except ObjectDoesNotExist:
        raise ex.NotExistStudentList()

    with transaction.atomic():
        updated_student_list.name = student_list.name
        if student_list.is_main:
            tmp = StudentList.objects.get(user=user, is_main=True)
            tmp.is_main = False
            tmp.save()
        updated_student_list.is_main = student_list.is_main
        updated_student_list.has_allergy = student_list.has_allergy
        updated_student_list.save()
        for column in student_list.columns:
            try:
                col = Column.objects.get(
                    id=column.id, student_list=updated_student_list
                )
            except ObjectDoesNotExist:
                raise ex.NotFoundColumn()
            col.field = column.field
            col.save()

        for student in student_list.students:
            try:
                s = Student.objects.get(
                    id=student.id, student_list=updated_student_list
                )
            except ObjectDoesNotExist:
                raise ex.NotFoundStudent()
            s.number = student.number
            s.name = student.name
            s.gender = student.gender
            if updated_student_list.has_allergy and student.allergy:
                s.allergy.set([Allergy.objects.get(pk=a) for a in student.allergy])
            for row in student.rows:
                try:
                    r = Row.objects.get(column=col, student=s)
                    r.value = row.value
                    r.save()
                except ObjectDoesNotExist:
                    raise ex.NotFoundStudent()
            s.save()

    res_students = []
    for s in updated_student_list.student_set.all():
        res_rows = []
        for r in s.row_set.all():
            res_row = studentList_schemas.Row(id=col.id, value=r.value)
            res_rows.append(res_row)
        res_student = studentList_schemas.StudentWithRows(
            id=s.id,
            number=s.number,
            name=s.name,
            gender=s.gender,
            allergy=[e.code for e in s.allergy.all()],
            rows=res_rows,
        )
        res_students.append(res_student)

    res_student_list = studentList_schemas.StudentListWithStudent(
        id=updated_student_list.id,
        name=updated_student_list.name,
        is_main=updated_student_list.is_main,
        has_allergy=updated_student_list.has_allergy,
        created_at=updated_student_list.created_at,
        updated_at=updated_student_list.updated_at,
        columns=[
            studentList_schemas.Column(id=e.id, field=e.field)
            for e in updated_student_list.column_set.all()
        ],
        students=res_students,
    )

    return ResponseWrapper(res_student_list)


# @router.post(
#     "/columns",
#     status_code=status.HTTP_201_CREATED,
#     response_model=ResponseModel[schemas.StudentListWithStudent],
# )
# async def columns(
#     columns: schemas.ColumnCreate,
#     db: Session = Depends(get_db),
#     token_email: str = Depends(user_email),
# ):
#     """
#     Request body 예시\n
#     {\n
#     \t"field": "전화번호",\n
#     \t"student_list_id": 9,\n
#     \t"student_id": [1, 2, 3]\n
#     }
#     """
#     return ResponseWrapper(crud.create_column(db, token_email, columns))


# @router.put(
#     "/columns",
#     status_code=status.HTTP_200_OK,
#     response_model=ResponseModel[schemas.StudentListWithStudent],
# )
# async def columns(
#     column: schemas.ColumnUpdate,
#     db: Session = Depends(get_db),
#     token_email: str = Depends(user_email),
# ):
#     """
#     {\n
#         "field": "전화번호", // 명렬표에 존재하는 필드네임
#         "studentListId": 54, // 명렬표 id
#         "studentId": [
#             53, 54, 55 // 명렬표에 포함된 학생 id
#         ],
#         "value": [
#             "112", "114", "119" // 학생 순서대로 필드값
#         ]
#     }
#     """
#     return ResponseWrapper(crud.update_column(db, column, token_email))