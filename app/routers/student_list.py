from fastapi import Depends, APIRouter, status, Query, Body
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..schemas import ResponseModel, ResponseWrapper
from ..dependencies import get_db, user_email

router = APIRouter(prefix="/student", tags=["Student"])


# 명렬표
@router.get(
    "/list", status_code=200, response_model=ResponseModel[list[schemas.StudentList]]
)
async def student_list(
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    """
    모든 명렬표 보기(학생은 안보임)\n
    로그인만 하면 별도의 파라미터 없음
    """
    return ResponseWrapper(crud.get_student_lists(db, token_email))


@router.get(
    "/list/{list_id}",
    status_code=200,
    response_model=ResponseModel[schemas.StudentListWithStudent],
)
async def student_list(
    list_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    """
    특정 명렬표 보기(학생까지 보임)\n
    파라미터 값은 명렬표 id
    """
    return ResponseWrapper(crud.get_student_list(db, token_email, list_id))


@router.post(
    "/list",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[schemas.StudentList],
)
async def student_list(
    student_list: schemas.StudentListCreate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    """
    {\n
        "name": "3-2반 명렬표", // 명렬표 이름
        "isMain": false, // 메인 명렬표 여부
        "description": "우리반 명렬표", // 명렬표 설명
        "hasAllergy": false, // 알러지 정보 사용 여부
        "students": [ // 학생 정보 입력
            {
                "number": 1, // 번호
                "name": "김개똥", // 학생 이름
                "isMale": true, // 성별(true: 남자, false: 여자)
                "description": "맨 앞자리", // 학생 설명
                "allergy": [] // 알러지 정보, 없으면 빈 배열
            },
            {
                "number": 2, // 번호
                "name": "나승범", // 학생 이름
                "isMale": false, // 성별(true: 남자, false: 여자)
                "description": "급식 1번", // 학생 설명
                "allergy": [1, 2, 3] // 알러지 정보, 없으면 빈 배열
            },
        ]
    }
    """
    return ResponseWrapper(crud.create_student_list(db, token_email, student_list))


@router.delete("/list/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def student_list(
    list_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    """
    명렬표 지우기(학생까지 다 지워짐)\n
    파라미터 값은 명렬표 id
    """
    return ResponseWrapper(crud.delete_student_list(db, token_email, list_id))


@router.put(
    "/list/{list_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.StudentList],
)
async def student_list(
    list_id: int,
    student_list: schemas.StudentListUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    """
    {\n
        "name": "새로운 명렬표 이름",
        "isMain": true,
        "description": "새로운 명렬표 설명",
        "hasAllergy": true
    }
    """
    return ResponseWrapper(
        crud.update_student_list(db, token_email, list_id, student_list)
    )


@router.post(
    "/columns",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[schemas.StudentListWithStudent],
)
async def columns(
    columns: schemas.ColumnCreate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    """
    Request body 예시\n
    {\n
    \t"field": "전화번호",\n
    \t"student_list_id": 9,\n
    \t"student_id": [1, 2, 3]\n
    }
    """
    return ResponseWrapper(crud.create_column(db, token_email, columns))


@router.put(
    "/columns",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.StudentListWithStudent],
)
async def columns(
    column: schemas.ColumnUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    """
    {\n
        "field": "전화번호", // 명렬표에 존재하는 필드네임
        "studentListId": 54, // 명렬표 id
        "studentId": [
            53, 54, 55 // 명렬표에 포함된 학생 id
        ],
        "value": [
            "112", "114", "119" // 학생 순서대로 필드값
        ]
    }
    """
    return ResponseWrapper(crud.update_column(db, column, token_email))


@router.get(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.Student],
)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.get_student(db, token_email, student_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseModel[schemas.Student],
)
async def student(
    list_id: int = Query(..., alias="listId"),
    student: schemas.StudentCreate = Body(...),
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.create_student(db, token_email, list_id, student))


@router.put(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseModel[schemas.Student],
)
async def student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.update_student(db, token_email, student_id, student))


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def student(
    student_id: int,
    db: Session = Depends(get_db),
    token_email: str = Depends(user_email),
):
    return ResponseWrapper(crud.delete_student(db, token_email, student_id))
