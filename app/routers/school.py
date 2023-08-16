from fastapi import Query, HTTPException, APIRouter
from fastapi.responses import JSONResponse
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
def lunchMenuToDict(str):
    splited = str.split(" ")
    return {
        "menu": splited[0],
        "allergy": []
        if not splited[1]
        else list(map(int, splited[1].strip("(" ")").split("."))),
    }


def originToDict(str):
    splited = str.split(" : ")
    return {"ingredient": splited[0], "origin": splited[1]}


@router.get("/lunch-menu", status_code=200, response_model=schemas.SchoolLunch)
async def schoolLunch(
    areaCode: str | None,
    schoolCode: int | None,
    date: Annotated[int | None, Query(ge=10000000, lt=100000000)],
):
    params = base_params.copy()
    params.update(
        {"ATPT_OFCDC_SC_CODE": areaCode, "SD_SCHUL_CODE": schoolCode, "MLSV_YMD": date}
    )
    response = requests.get(
        f"{NICE_URL}/mealServiceDietInfo", base_params=params
    ).json()
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
    row = response["mealServiceDietInfo"][1]["row"][0]
    lunchMenu = list(map(lunchMenuToDict, row["DDISH_NM"].split("<br/>")))
    origin = list(map(originToDict, row["ORPLC_INFO"].split("<br/>")))
    return JSONResponse(
        status_code=200, content={"lunchMenu": lunchMenu, "origin": origin}
    )
