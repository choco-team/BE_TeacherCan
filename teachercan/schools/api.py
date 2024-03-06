from ninja import Router, Query

from .schemas import SchoolIn

router = Router(tags=["School"])


@router.get("/list")
def list_school(reqeust, payload=Query[SchoolIn]):
    return ...


@router.get("/lunch-menu")
def list_lunch_menu(request, payload=Query[SchoolIn]):
    return ...
