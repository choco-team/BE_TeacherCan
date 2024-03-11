from ninja import Router

from ..auths.api import AuthBearer
from .models import User
from .schemas import InfoIn, InfoOut
from ..schools.models import School
from ..schools.api import create_school

router = Router(auth=AuthBearer(), tags=["User"])


# 1.개인 정보 조회
@router.get("/info", response=InfoOut)
def get_user(request):
    return request.auth


# # 2.개인 정보 수정
@router.put("/info", response=InfoOut)
def put_user(request, payload: InfoIn):
    user: User = request.auth
    for attr, value in payload.dict().items():
        setattr(user, attr, value)
    try:
        school = School.objects.get(pk=payload.school_code)
    except:
        school = create_school(payload.school_code)
    user.school = school
    user.save()
    return user
