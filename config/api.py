from ninja import NinjaAPI
from config.renderers import DefaultRenderer
from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router

from config import exceptions as ex

api = NinjaAPI(renderer=DefaultRenderer())

# 기본내장 예외 처리


@api.exception_handler(Exception)
def exception_handelr(request, exc):
    return ex.exception_handelr(request, exc, api)

# 커스텀 예외 처리


@api.exception_handler(ex.APIException)
def exception_handelr(request, exc):
    return ex.api_exception_handelr(request, exc, api)


api.add_router("/auth/", auth_router)
api.add_router("/user/", user_router)
