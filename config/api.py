from ninja import NinjaAPI

from teachercan.auths.api import router as auth_router
from teachercan.users.api import router as user_router
from teachercan.schools.api import router as school_router
from teachercan.students.api import router as student_router

api = NinjaAPI()

api.add_router("/auth/", auth_router)
api.add_router("/user/", user_router)
api.add_router("/school/", school_router)
api.add_router("/student/", student_router)
