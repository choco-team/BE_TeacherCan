from django.template import TemplateSyntaxError
from ninja import NinjaAPI
from ninja.errors import AuthenticationError, ValidationError, HttpError

from config import exceptions as ex
from config.renderers import DefaultRenderer
from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router
from teachercan.students.api import router as student_router
from teachercan.schools.api import router as school_router
from teachercan.student_lists.api import router as student_list_router
from teachercan.columns.api import router as column_router


api = NinjaAPI(renderer=DefaultRenderer())


# token인증 예외처리
@api.exception_handler(AuthenticationError)
def auth_unavailable(request, exc):
    return api.create_response(
        request, {"code": 1001, "message": "로그인이 필요한 서비스에요."}, status=401
    )


# 커스텀 예외처리
@api.exception_handler(ex.APIException)
def exception_handelr(request, exc):
    return ex.api_exception_handelr(request, exc, api)


# 유효성검사 예외처리
@api.exception_handler(ValidationError)
def exception_handelr(request, exc):
    return ex.validation_exception_handelr(request, exc, api)


# 기본내장 예외처리(응답 ValidationError 포함)
@api.exception_handler(Exception)
def exception_handelr(request, exc):
    return ex.exception_handelr(request, exc, api)


# HttpError (requestbody json 형식이 잘못 됐을 때 발생)
@api.exception_handler(HttpError)
def exception_handelr(request, exc):
    return ex.exception_handelr(request, exc, api, status=400, code=1002)

api.add_router("/auth/", auth_router)
api.add_router("/user/", user_router)
api.add_router("/student/", student_router)
api.add_router("/school/", school_router)
api.add_router("/student/list/", student_list_router)
api.add_router("/column/", column_router)
