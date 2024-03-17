from teachercan.students.models import Student
from . import schemas
from .models import StudentList
from ..auths.api import AuthBearer
from ninja import Router
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

router = Router(auth=AuthBearer(), tags=["StudentList"])

# 명렬표
@router.get("", response=schemas.GetStudentList)
def get_student_list(request):
    """
    모든 명렬표 보기(학생은 안보임)\n
    로그인만 하면 별도의 파라미터 없음
    """
    return {"studentList": StudentList.objects.filter(user=request.auth)}

# @router.get(
#     "/{list_id}",
#     status_code=200,
#     response_model=ResponseModel[studentList_schemas.StudentListWithStudent],
# )
# def student_list(list_id: int, user: str = Depends(user)):
#     """
#     특정 명렬표 보기(학생까지 보임)\n
#     파라미터 값은 명렬표 id
#     """
#     try:
#         q = StudentList.objects.get(id=list_id, user=user)
#     # 명렬표 없을 때 예외 처리
#     except ObjectDoesNotExist:
#         raise ex.NotExistStudentList()
#     columns = [
#         studentList_schemas.Column(id=column.id, field=column.field)
#         for column in q.column_set.all()
#     ]
#     students = [
#         studentList_schemas.StudentWithRows(
#             id=e.id,
#             number=e.number,
#             name=e.name,
#             gender=e.gender,
#             allergy=[a.code for a in e.allergy.all()] if q.has_allergy else None,
#             rows=[{"id": r.column.id, "value": r.value}
#                   for r in e.row_set.all()],
#         )
#         for e in q.student_set.all()
#     ]
#     return ResponseWrapper(
#         studentList_schemas.StudentListWithStudent(
#             id=q.id,
#             name=q.name,
#             is_main=q.is_main,
#             has_allergy=q.has_allergy,
#             created_at=q.created_at,
#             updated_at=q.updated_at,
#             columns=columns,
#             students=students,
#         )
#     )


# @router.post("",response=schemas.StudentListWithStudent)
@router.post("")
# ,response=schemas.StudentListWithStudent
def post_student_list(request, student_list_create: schemas.StudentListCreate,):
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
            },
        ]
    }
    """
    user = request.auth
    new_student_list = StudentList(
        name=student_list_create.name,
        has_allergy=False,
        is_main=not user.studentlist_set.count(),
        user=user,
    )
    students = [
        Student(
            number=s.number, name=s.name, gender=s.gender, student_list=new_student_list
        )
        for s in student_list_create.students
    ]
    with transaction.atomic():
        new_student_list.save()
        for s in students:
            s.save()
    # asd = StudentList.objects.prefetch_related('student_set').filter(id=new_student_list.id)
    print(new_student_list.student_set.all())
    return "asd"



# @router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
# def student_list(
#     list_id: int,
#     user: str = Depends(user),
# ):
#     """
#     명렬표 지우기(학생까지 다 지워짐)\n
#     파라미터 값은 명렬표 id
#     """
#     try:
#         student_list = StudentList.objects.get(id=list_id, user=user)
#     except ObjectDoesNotExist:
#         raise ex.NotFoundStudentList()
#     student_list.delete()
#     return ResponseWrapper(data=None)


# @router.put(
#     "/main",
#     status_code=status.HTTP_200_OK,
#     response_model=ResponseModel[str],
# )
# def put_student_list_main(
#     update_main: studentList_schemas.UpdateMain,
#     user: str = Depends(user)
# ):
#     try:
#         updated_student_list = StudentList.objects.get(
#             id=update_main.id, user=user)
#         tmp = StudentList.objects.get(user=user, is_main=True)
#     except ObjectDoesNotExist:
#         raise ex.NotExistStudentList()
#     tmp.is_main = False
#     updated_student_list.is_main = update_main.isMain
#     tmp.save()
#     updated_student_list.save()

#     return ResponseWrapper("성공적으로 변경 되었습니다.")


# @router.put(
#     "/",
#     status_code=status.HTTP_200_OK,
#     response_model=ResponseModel[studentList_schemas.StudentListWithStudent],
# )
# def student_list(
#     student_list: studentList_schemas.StudentListUpdate,
#     user: str = Depends(user),
# ):
#     try:
#         updated_student_list = StudentList.objects.get(
#             id=student_list.id, user=user)
#     except ObjectDoesNotExist:
#         raise ex.NotExistStudentList()

#     with transaction.atomic():
#         updated_student_list.name = student_list.name
#         if student_list.is_main:
#             tmp = StudentList.objects.get(user=user, is_main=True)
#             tmp.is_main = False
#             tmp.save()
#         updated_student_list.is_main = student_list.is_main
#         updated_student_list.has_allergy = student_list.has_allergy
#         updated_student_list.save()
#         for column in student_list.columns:
#             try:
#                 col = Column.objects.get(
#                     id=column.id, student_list=updated_student_list
#                 )
#             except ObjectDoesNotExist:
#                 raise ex.NotFoundColumn()
#             col.field = column.field
#             col.save()

#         for student in student_list.students:
#             try:
#                 s = Student.objects.get(
#                     id=student.id, student_list=updated_student_list
#                 )
#             except ObjectDoesNotExist:
#                 raise ex.NotFoundStudent()
#             s.number = student.number
#             s.name = student.name
#             s.gender = student.gender
#             if updated_student_list.has_allergy and student.allergy:
#                 s.allergy.set([Allergy.objects.get(pk=a)
#                               for a in student.allergy])
#             for row in student.rows:
#                 try:
#                     r = Row.objects.get(column=col, student=s)
#                     r.value = row.value
#                     r.save()
#                 except ObjectDoesNotExist:
#                     raise ex.NotFoundStudent()
#             s.save()

#     res_students = []
#     for s in updated_student_list.student_set.all():
#         res_rows = []
#         for r in s.row_set.all():
#             res_row = studentList_schemas.Row(id=col.id, value=r.value)
#             res_rows.append(res_row)
#         res_student = studentList_schemas.StudentWithRows(
#             id=s.id,
#             number=s.number,
#             name=s.name,
#             gender=s.gender,
#             allergy=[e.code for e in s.allergy.all()],
#             rows=res_rows,
#         )
#         res_students.append(res_student)

#     res_student_list = studentList_schemas.StudentListWithStudent(
#         id=updated_student_list.id,
#         name=updated_student_list.name,
#         is_main=updated_student_list.is_main,
#         has_allergy=updated_student_list.has_allergy,
#         created_at=updated_student_list.created_at,
#         updated_at=updated_student_list.updated_at,
#         columns=[
#             studentList_schemas.Column(id=e.id, field=e.field)
#             for e in updated_student_list.column_set.all()
#         ],
#         students=res_students,
#     )

#     return ResponseWrapper(res_student_list)
