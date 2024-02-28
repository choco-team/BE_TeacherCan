from ninja import NinjaAPI

from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router

api = NinjaAPI()

api.add_router("/auth/", auth_router, tags=["auth"])
api.add_router("/user/", user_router, tags=["user"])
