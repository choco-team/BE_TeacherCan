from typing import Annotated
from enum import Enum
from datetime import date, timedelta, datetime

from fastapi import Depends, Query, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
import requests

from .. import crud, schemas
from ..common.consts import NICE_API_KEY, NICE_URL
from ..dependencies import get_db
from .auth import verify_token


router = APIRouter(prefix="/school", tags=["school"])


base_params = {"Type": "json", "KEY": NICE_API_KEY}


# 1. 학교정보 - 1. 학교 정보 검색
@router.get("/list", status_code=200, response_model=schemas.SchoolLists)
async def school_list(
    school_name: str | None = Query(None, alias="schoolName"),
    page_number: int | None = Query(1, alias="pageNumber"),
    data_size: int | None = Query(10, alias="dataSize"),
):
    return crud.api_search_schools(
        name=school_name, page_number=page_number, data_size=data_size
    )


# 2. 급식정보 - 1. 급식 정보 조회
class MenuType(Enum):
    weekend = "weekend"
    day = "day"


@router.get("/lunch-menu", status_code=200, response_model=list[schemas.SchoolMeal])
async def get_menu(
    date: Annotated[date | None, Query()],
    type: MenuType,
    db: Session = Depends(get_db),
    token_email: str = Depends(verify_token),
):
    # 유저 정보 불러오기 from token
    db_user = crud.get_user(db, email=token_email)
    if not db_user.school:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No registered school information.",
        )

    # 파라미터 생성
    params = base_params.copy()
    start_date = date if type == MenuType.day else date - timedelta(date.weekday())
    end_date = date if type == MenuType.day else start_date + timedelta(4)
    areaCode = db_user.school.area_code
    schoolCode = db_user.school.code
    params.update(
        {
            "ATPT_OFCDC_SC_CODE": areaCode,
            "SD_SCHUL_CODE": schoolCode,
            "MLSV_FROM_YMD": start_date.strftime("%Y%m%d"),
            "MLSV_TO_YMD": end_date.strftime("%Y%m%d"),
        }
    )

    # 외부 api 호출
    response = requests.get(f"{NICE_URL}/mealServiceDietInfo", params=params).json()
    try:
        response["mealServiceDietInfo"]

    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        if code == 200:  # 200: 해당하는 데이터가 없습니다.
            return []
        else:
            raise HTTPException(
                status_code=500, detail={"code": 500, "message": "내부 API호출 실패"}
            )

    # 스키마에 맞게 데이터 수정
    res_menu: list[str] = response["mealServiceDietInfo"][1]["row"]

    for menu in res_menu:
        try:
            menu["meal_type"] = menu["MMEAL_SC_NM"]
            menu["date"] = datetime.strptime(menu["MLSV_YMD"], "%Y%m%d").date()
            menu["menu"] = [
                {
                    "dish": dish,
                    "allergy": [
                        int(allergy)
                        for allergy in allergies.strip("()").split(".")
                        if allergy
                    ],
                }
                for dish, *_, allergies in [
                    dish_info.split(" ")
                    for dish_info in menu["DDISH_NM"].split("<br/>")
                ]
            ]
            menu["origin"] = [
                {"ingredient": ingredient, "place": place}
                for ingredient, *_, place in [
                    origin.split(" : ") for origin in menu["ORPLC_INFO"].split("<br/>")
                ]
            ]
        except:
            print(f"급식 데이터 파싱 실패, {res_menu}")
            return []
    return res_menu
