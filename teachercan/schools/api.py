from datetime import datetime, timedelta

from ninja import Router, Query
import requests

from config.settings import NICE_API_KEY, NICE_URL
from .schemas import SchoolIn, LunchIn, SchoolListOut, DayOrWeek, LunchOut
from .models import School
from ..auths.api import AuthBearer

router = Router(tags=["School"])
base_params = {"Type": "json", "KEY": NICE_API_KEY}


# 나이스 api 요청
def api_search_schools(
    page_number: int,
    data_size: int,
    school_name: str | None = None,
    code: str | None = None,
) -> list[dict]:
    params = base_params.copy()
    params.update(
        {
            "SD_SCHUL_CODE": code,
            "SCHUL_NM": school_name,
            "pindex": page_number,
            "pSize": data_size,
        }
    )
    try:
        response = requests.get(f"{NICE_URL}/schoolInfo", params=params).json()
    except:
        raise Exception("나이스 요청 에러")

    try:
        school_info = response["schoolInfo"]
        total = int(school_info[0]["head"][0]["list_total_count"])
        schools = [
            {
                "name": school["SCHUL_NM"],
                "address": school["ORG_RDNMA"],
                "code": school["SD_SCHUL_CODE"],
                "area_code": school["ATPT_OFCDC_SC_CODE"],
            }
            for school in school_info[1]["row"]
        ]
        res = {
            "school_list": schools,
            "pagination": {
                "page_number": page_number,
                "data_size": data_size,
                "total_page_number": -(-total // data_size),
            },
        }
        return res

    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        # 200: 해당하는 데이터가 없습니다. / 336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다
        if code == 200:
            # raise ex.NotFoundSchool()
            raise Exception("해당 학교 없음")
        elif code == 336:
            # raise ex.TooLargeEntity()
            raise Exception("데이터 요청 초과")
        else:
            raise Exception()


def create_school(code: str) -> School:
    school = api_search_schools(page_number=1, data_size=1, code=code)['school_list'][0]
    db_school = School(
        code=code,
        name=school["name"],
        area_code=school["area_code"],
        address=school["address"],
    )
    db_school.save()
    return db_school


@router.get("/list", response=SchoolListOut)
def list_school(request, payload: Query[SchoolIn]):
    return api_search_schools(**payload.dict())


@router.get("/lunch-menu", auth=AuthBearer(), response=list[LunchOut])
def list_lunch_menu(request, payload: Query[LunchIn]):
    print(payload)
    user = request.auth
    if not user.school:
        raise Exception("유저의 학교 정보 없음")

    if payload.type == DayOrWeek.day:
        start_date = payload.date
        end_date = payload.date
    else:
        start_date = payload.date - timedelta(payload.date.weekday())
        end_date = start_date + timedelta(4)

    params = base_params.copy()
    params.update(
        {
            "ATPT_OFCDC_SC_CODE": user.school.area_code,
            "SD_SCHUL_CODE": user.school.code,
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
            raise Exception("나이스 api 에러")

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
