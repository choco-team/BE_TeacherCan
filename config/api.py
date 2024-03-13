from ninja import NinjaAPI
from ninja.errors import AuthenticationError, ValidationError

from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router
from teachercan.schools.api import router as school_router
from teachercan.students.api import router as student_router
from .renderers import DefaultRenderer
from .exceptions import DefaultError

api = NinjaAPI(renderer=DefaultRenderer())


# 라우터 추가
api.add_router("/auth/", auth_router)
api.add_router("/user/", user_router)
api.add_router("/school/", school_router)
api.add_router("/student/", student_router)


# token 인증 실패 예외처리
@api.exception_handler(AuthenticationError)
def auth_unavailable(request, exc):
    return api.create_response(
        request, {"code": 1001, "message": "로그인이 필요한 서비스에요."}, status=401
    )


# 기본적인 예외 처리, config.exceptions
@api.exception_handler(DefaultError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": exc.message, "code": exc.code},
        status=exc.status_code,
    )


# 유효성 검사 실패 예외 처리
@api.exception_handler(ValidationError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {
            "message": "유효성 검사에서 문제가 발생했어요.",
            "code": 1003,
            "data": {"detail": exc.errors},
        },
        status=422,
    )


# 기타 예외 처리(모든 예외 catch하는지 확인 필요)
@api.exception_handler(Exception)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {
            "message": "서버에서 에러가 생겼어요.",
            "code": 1000,
            "data": {"detail": exc.__str__()},
        },
        status=500,
    )
