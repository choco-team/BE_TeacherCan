from ninja import Router

from ..auths.api import AuthBearer
from .models import User
from .schemas import InfoOut

router = Router(auth=AuthBearer(), tags=["User"])


# 1.개인 정보 조회
@router.get("/info", response=InfoOut)
def my_info(request):
    return request.auth


# # 2.개인 정보 수정
# @router.put(
#     "/info",
#     response_model=ResponseModel[user_schemas.User],
# )
# async def my_info(
#     user: user_schemas.UserUpdate,
#     db: Session = Depends(get_db),
#     token_email: str = Depends(user_email),
# ):
#     db_user = user_crud.update_user(db, email=token_email, user=user)
#     return ResponseWrapper(db_user)
