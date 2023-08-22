from enum import Enum
from datetime import date, timedelta, datetime

from fastapi import Query, HTTPException, APIRouter
from typing import Annotated
import requests

from .. import schemas, crud
from ..common.consts import NICE_API_KEY, NICE_URL


router = APIRouter(prefix="/school", tags=["school"])


base_params = {"Type": "json", "KEY": NICE_API_KEY}


# 1. 학교정보 - 1. 학교 정보 검색
@router.get("/list", status_code=200, response_model=schemas.SchoolLists)
# schoolName = None : 모든 학교를 ㄱㄴㄷ 순으로 응답
async def schoolList(
    schoolName: str | None = None, pageNumber: int | None = 1, dataSize: int | None = 10
):
    return crud.api_search_schools(
        name=schoolName, page_number=pageNumber, data_size=dataSize
    )


# 2. 급식정보 - 1. 급식 정보 조회
class MenuType(Enum):
    weekend = "weekend"
    day = "day"


@router.get("/lunch-menu", status_code=200, response_model=list[schemas.SchoolMeal])
async def get_menu(
    areaCode: str | None,
    schoolCode: int | None,
    date: Annotated[date | None, Query()],
    type: MenuType,
):
    # 파라미터 생성
    params = base_params.copy()
    start_date = date if type == "day" else date - timedelta(date.weekday())
    end_date = date if type == "day" else start_date + timedelta(4)
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
            raise HTTPException(
                status_code=400,
                detail={"code": 400, "message": response["RESULT"]["MESSAGE"]},
            )
        else:
            raise HTTPException(
                status_code=500, detail={"code": 500, "message": "내부 API호출 실패"}
            )

    # 스키마에 맞게 데이터 수정
    res_menu: list[str] = response["mealServiceDietInfo"][1]["row"]
    for menu in res_menu:
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
                dish_info.split(" ") for dish_info in menu["DDISH_NM"].split("<br/>")
            ]
        ]
        menu["origin"] = [
            {"ingredient": ingredient, "place": place}
            for ingredient, *_, place in [
                origin.split(" : ") for origin in menu["ORPLC_INFO"].split("<br/>")
            ]
        ]
    return res_menu
