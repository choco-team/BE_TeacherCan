from ninja import Router

router = Router(tags=["School"])


@router.get("/list")
def list_school():
    return ...


@router.get("/lunch-menu")
def list_lunch_menu():
    return ...
