from django.contrib.auth.hashers import (
    make_password,
    check_password,
)

from fastapi import Query, Depends,  HTTPException, APIRouter
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session

from ..dependencies import get_db
from .. import schemas, crud

import math
import environ
import requests


router = APIRouter(
    prefix="/school",
    tags = ["school"]
)

# 환경변수 init
env = environ.Env()
env.read_env(env.str("ENV_PATH", ".env"))

# school
niceKEY = env("NICE_API_KEY")
niceURL = "https://open.neis.go.kr/hub"
params = {"Type": "json", "KEY": niceKEY}

# 1. 학교정보 - 1. 학교 정보 검색
def filterSchoolList(school):
    return {
        "schoolName": school["SCHUL_NM"],
        "schoolAddress": school["ORG_RDNMA"],
        "schoolCode": school["SD_SCHUL_CODE"],
        "areaCode": school["ATPT_OFCDC_SC_CODE"]
    }

@router.get("/list", status_code=200, response_model=schemas.SchoolLists)
# schoolName = None : 모든 학교를 ㄱㄴㄷ 순으로 응답
async def schoolList(schoolName: str | None = None, pageNumber: int | None = 1, dataSize: int | None = 10):
    print(params)
    nParams = params.copy()
    nParams.update(
        {"SCHUL_NM": schoolName, "pIndex": pageNumber, "pSize": dataSize})
    response = requests.get(f"{niceURL}/schoolInfo", params=nParams).json()
    try:
        response["schoolInfo"]
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        if code == 200 or code == 336:  # 200: 해당하는 데이터가 없습니다. / 336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다
            raise HTTPException(status_code=400, detail={
                                "code": 400, "message": response["RESULT"]["MESSAGE"]})
        else:
            raise HTTPException(status_code=500, detail={
                                "code": 500, "message": "내부 API호출 실패"})
    schoolList = list(map(filterSchoolList, response["schoolInfo"][1]["row"]))
    totalPageNumber = math.ceil(
        response["schoolInfo"][0]["head"][0]["list_total_count"]/dataSize)
    return JSONResponse(status_code=200, content={
        "schoolList": schoolList,
        "pagination": {
            "pageNumber": pageNumber,
            "dataSize": dataSize,
            "totalPageNumber": totalPageNumber,
        }
    }
    )


# 2. 급식정보 - 1. 급식 정보 조회
def lunchMenuToDict(str):
    splited = str.split(" ")
    return {"menu": splited[0], "allergy": [] if not splited[1] else list(map(int, splited[1].strip("("")").split(".")))}

def originToDict(str):
    splited = str.split(" : ")
    return {"ingredient": splited[0], "origin": splited[1]}

@router.get("/lunch-menu", status_code=200, response_model=schemas.SchoolLunch)
async def schoolLunch(areaCode: str | None, schoolCode: int | None, date: Annotated[int | None, Query(ge=10000000, lt=100000000)]):
    nParams = params.copy()
    nParams.update(
        {"ATPT_OFCDC_SC_CODE": areaCode, "SD_SCHUL_CODE": schoolCode, "MLSV_YMD": date})
    response = requests.get(
        f"{niceURL}/mealServiceDietInfo", params=nParams).json()
    try:
        response["mealServiceDietInfo"]
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        if code == 200:  # 200: 해당하는 데이터가 없습니다.
            raise HTTPException(status_code=400, detail={
                                "code": 400, "message": response["RESULT"]["MESSAGE"]})
        else:
            raise HTTPException(status_code=500, detail={
                                "code": 500, "message": "내부 API호출 실패"})
    row = response["mealServiceDietInfo"][1]["row"][0]
    lunchMenu = list(map(lunchMenuToDict, row["DDISH_NM"].split("<br/>")))
    origin = list(map(originToDict, row["ORPLC_INFO"].split("<br/>")))
    return JSONResponse(status_code=200, content={
        "lunchMenu": lunchMenu,
        "origin": origin
    })

# school_code로 학교정보 가져오기? 아직 안쓰임. 미완성인듯?
@router.get("/{school_code}", response_model=schemas.School)
def read_school(school_code: str, db: Session = Depends(get_db)):
    db_school = crud.get_school(db, school_code=school_code)
    password = "1234"
    hashed_password = make_password(password)
    print(check_password(password, hashed_password))
    print(db_school.users)
    return db_school
