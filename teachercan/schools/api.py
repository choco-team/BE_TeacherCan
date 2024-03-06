from ninja import Router, Query

from .schemas import SchoolIn, LunchIn

router = Router(tags=["School"])


@router.get("/list")
def list_school(request, payload: Query[SchoolIn]):
    return None


@router.get("/lunch-menu")
def list_lunch_menu(request, payload: Query[LunchIn]):
    return ...
