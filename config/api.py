from ninja import NinjaAPI
from config.exceptions import ServiceUnavailableError

from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router

api = NinjaAPI()

@api.exception_handler(ServiceUnavailableError)
def service_unavailable(request, exc):
    return api.create_response(
        request,
        {"message": "Please retry later"},
        status=503,
    )


api.add_router("/auth/", auth_router, tags=["auth"])
api.add_router("/user/", user_router, tags=["user"])
