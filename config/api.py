from ninja import NinjaAPI
from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router

from config import exceptions as ex

api = NinjaAPI()

@api.exception_handler(ex.APIException)
def exception_handelr(request, exc):
    return ex.api_exception_handelr(request, exc, api)


api.add_router("/auth/", auth_router, tags=["auth"])
api.add_router("/user/", user_router, tags=["user"])
