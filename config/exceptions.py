from rest_framework import status

def api_exception_handelr(request, exc, api):
    return api.create_response(
        request,
        {
            "code": exc.code,
            "message": exc.message,
        },
        status=exc.status_code,
    )


def exception_handelr(request, exc, api):
    data = {
        "detail": None,
        "path": request.path,
        "method": request.method,
        "path_params": request.resolver_match.kwargs if request.resolver_match.kwargs else None,
        "query_params": request.environ['QUERY_STRING'] if request.environ['QUERY_STRING'] else None,
        "body": request.body.decode() if request.body.decode() else None,
    }
    try:
        data['detail'] = exc.errors()[0]
    except:
        data['detail'] = f"{exc.__str__()} {str(exc.__context__)}"
    print("💣 서버 에러 발생!!!!\n", data)

    return api.create_response(
        request,
        {
            "code": 1000,
            "message": "서버에서 에러가 발생했어요.",
            "data": data
        },
        status=500,
    )


def validation_exception_handelr(request, exc, api):
    data = {
        "detail": exc.errors[0],
        "path": request.path,
        "method": request.method,
        "path_params": request.resolver_match.kwargs if request.resolver_match.kwargs else None,
        "query_params": request.environ['QUERY_STRING'] if request.environ['QUERY_STRING'] else None,
        "body": request.body.decode() if request.body.decode() else None,
    }
    print("💣 ValidationError 발생!!!!\n", data)
    return api.create_response(
        request,
        {
            "code": 1000,
            "message": "유효성 검사에서 문제가 발생했어요.",
            "data": data
        },
        status=500,
    )


class APIException(Exception):    
    def __init__(
        self,
        code:int = 1000, 
        message:str = "서버 에러",
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, 
    ):        
        self.code = code
        self.message = message
        self.status_code = status_code

# Auth
invalid_token = APIException(1002, "유효하지 않은 토큰이에요.", 401)
email_already_exist = APIException(1102, "이메일이 이미 존재해요.", 409)

# 공통
server_error = APIException()
not_authenticated = APIException(
    1001, "로그인이 필요한 서비스예요.", status.HTTP_403_FORBIDDEN)
invalid_token = APIException(
    1002, "유효하지 않은 토큰이에요.", status.HTTP_403_FORBIDDEN)

# Auth
email_already_exist = APIException(
    1102, "이메일이 이미 존재해요.", status.HTTP_409_CONFLICT)
password_invalid = APIException(
    1103, "비밀번호는 8자 보다 적거나, 너무 일반적인 단어는 안 돼요.", status.HTTP_422_UNPROCESSABLE_ENTITY
)
not_found_user = APIException(
    1104, "이메일을 다시 확인해주세요.", status.HTTP_404_NOT_FOUND)
password_not_match = APIException(
    1105, "비밀번호를 다시 확인해주세요.", status.HTTP_401_UNAUTHORIZED
)

# School
nice_api_error = APIException(
    1301, "관련된 정보를 불러오는 중에 에러가 발생했어요.", status.HTTP_503_SERVICE_UNAVAILABLE
)
not_found_school = APIException(
    1302, "해당하는 학교 정보가 존재하지 않아요.", status.HTTP_404_NOT_FOUND
)
too_large_entity = APIException(
    1303, "데이터 요청은 한번에 1,000건을 넘을 수 없어요.", status.HTTP_400_BAD_REQUEST
)
not_regist_school = APIException(
    1304, "등록된 학교 정보가 없어요. 먼저 학교를 등록해주세요.", status.HTTP_404_NOT_FOUND
)

# Student
not_found_student_list = APIException(
    1401, "요청하신 명렬표가 존재하지 않아요.", status.HTTP_404_NOT_FOUND
)
not_exist_student_list = APIException(
    1402, "등록된 명렬표가 없어요. 먼저 명렬표를 등록해주세요.", status.HTTP_404_NOT_FOUND
)
not_found_student = APIException(
    1403, "해당하는 학생이 존재하지 않아요.", status.HTTP_404_NOT_FOUND
)

# Column
not_found_column = APIException(
    1501, "요청하신 column이 존재하지 않아요.", status.HTTP_404_NOT_FOUND
)

# 유효성 검사
request_default_error = APIException(
    1003, "유효성 검사에서 문제가 발생했어요.", status.HTTP_400_BAD_REQUEST
)
# path = {
#     "/api/auth/signup/validation": ErrorDetail(1101, "이메일이 형식이 올바르지 않아요."),
# }