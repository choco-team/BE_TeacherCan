from sqlalchemy import select
from sqlalchemy.orm import Session
import requests


from app import models
from app.common.consts import NICE_URL, NICE_API_KEY
from app.errors import exceptions as ex

from app.schemas import school_schemas

def api_search_schools(
    name: str | None = None,
    code: str | None = None,
    page_number: int | None = 1,
    data_size: int | None = 10,
) -> school_schemas.SchoolLists:
    params = {
        "Type": "json",
        "KEY": NICE_API_KEY,
        "SD_SCHUL_CODE": code,
        "SCHUL_NM": name,
        "pindex": page_number,
        "pSize": data_size,
    }
    try:
        response = requests.get(f"{NICE_URL}/schoolInfo", params=params).json()
    except:
        raise ex.NiceApiError()

    try:
        school_info = response["schoolInfo"]
        total = int(school_info[0]["head"][0]["list_total_count"])
        schools = [school_schemas.SchoolList(**school) for school in school_info[1]["row"]]
        return school_schemas.SchoolLists(
            **{
                "school_list": schools,
                "pagination": {
                    "page_number": page_number,
                    "data_size": data_size,
                    "total_page_number": -(-total // data_size),
                },
            }
        )
    except:
        code = int(response["RESULT"]["CODE"].split("-")[1])
        # 200: 해당하는 데이터가 없습니다. / 336: 데이터요청은 한번에 최대 1,000건을 넘을 수 없습니다
        if code == 200:
            raise ex.NotFoundSchool()
        elif code == 336:
            raise ex.TooLargeEntity()
        else:
            raise Exception()


def get_school(db: Session, code: str | None = None):
    result = db.query(models.School).filter(models.School.code == code).first()
    return result


def create_school(db: Session, code: str):
    school = api_search_schools(code=code).school_list[0]
    db_school = models.School(
        code=code, name=school.school_name, area_code=school.area_code
    )
    db.add(db_school)
    db.commit()
    db.refresh(db_school)