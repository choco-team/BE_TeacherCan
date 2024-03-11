from rest_framework import status

class Error:
    class ErrorDetail:
        def __init__(
            self,
            code: int,
            message: str,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        ):
            self.status_code = status_code
            self.code = code
            self.message = message

    default = ErrorDetail(1000, "서버에서 에러가 생겼어요. 에러 데이터를 티처캔으로 알려주세요.")

    # 공통
    server_error = default
    not_authenticated = ErrorDetail(1001, "로그인이 필요한 서비스예요.", status.HTTP_403_FORBIDDEN)
    invalid_token = ErrorDetail(1002, "유효하지 않은 토큰이에요.", status.HTTP_403_FORBIDDEN)

    # Auth
    email_already_exist = ErrorDetail(1102, "이메일이 이미 존재해요.", status.HTTP_409_CONFLICT)
    password_invalid = ErrorDetail(
        1103, "비밀번호는 8자 보다 적거나, 너무 일반적인 단어는 안 돼요.", status.HTTP_422_UNPROCESSABLE_ENTITY
    )
    not_found_user = ErrorDetail(1104, "이메일을 다시 확인해주세요.", status.HTTP_404_NOT_FOUND)
    password_not_match = ErrorDetail(
        1105, "비밀번호를 다시 확인해주세요.", status.HTTP_401_UNAUTHORIZED
    )

    # School
    nice_api_error = ErrorDetail(
        1301, "관련된 정보를 불러오는 중에 에러가 발생했어요.", status.HTTP_503_SERVICE_UNAVAILABLE
    )
    not_found_school = ErrorDetail(
        1302, "해당하는 학교 정보가 존재하지 않아요.", status.HTTP_404_NOT_FOUND
    )
    too_large_entity = ErrorDetail(
        1303, "데이터 요청은 한번에 1,000건을 넘을 수 없어요.", status.HTTP_400_BAD_REQUEST
    )
    not_regist_school = ErrorDetail(
        1304, "등록된 학교 정보가 없어요. 먼저 학교를 등록해주세요.", status.HTTP_404_NOT_FOUND
    )

    # Student
    not_found_student_list = ErrorDetail(
        1401, "요청하신 명렬표가 존재하지 않아요.", status.HTTP_404_NOT_FOUND
    )
    not_exist_student_list = ErrorDetail(
        1402, "등록된 명렬표가 없어요. 먼저 명렬표를 등록해주세요.", status.HTTP_404_NOT_FOUND
    )
    not_found_student = ErrorDetail(
        1403, "해당하는 학생이 존재하지 않아요.", status.HTTP_404_NOT_FOUND
    )

    #Column
    not_found_column = ErrorDetail(
        1501, "요청하신 column이 존재하지 않아요.", status.HTTP_404_NOT_FOUND
    )

    # 유효성 검사
    request_default_error = ErrorDetail(
        1003, "유효성 검사에서 문제가 발생했어요.", status.HTTP_400_BAD_REQUEST
    )
    path = {
        "/api/auth/signup/validation": ErrorDetail(1101, "이메일이 형식이 올바르지 않아요."),
    }


# async def request_exception_handelr(request: Request, exc: RequestValidationError):
#     path = request.url.path
#     error = Error.path.get(path)
#     if not error:
#         return JSONResponse(
#             status_code=Error.request_default_error.status_code,
#             content={
#                 "result": False,
#                 "code": Error.request_default_error.code,
#                 "message": Error.request_default_error.message,
#                 "data": exc.errors(),
#             },
#         )
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={
#             "result": False,
#             "code": error.code,
#             "message": error.message,
#             "data": exc.errors(),
#         },
#     )

async def response_exception_handelr(request, exc, api):
    data = {
        "path": request.url.path,
        "method": request.method,
        "path_params": request.path_params or None,
        "query_params": str(request.query_params) or None,
        "body": exc.body if hasattr(exc, "body") else None,
    }
    print("💣 서버 에러 발생!!!!\n", data)
    return api.create_response(
        status_code=Error.server_error.status_code,
        content={
            "success": False,
            "code": Error.server_error.code,
            "message": Error.server_error.message,
            "data": data,
        },
    )

def api_exception_handelr(request, exc: "APIException", api):
    return api.create_response(
        request,
        {  
            "success": exc.success,
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
        },
        status=exc.status_code,
    )

class APIException(Exception):
    success: bool
    status_code: int
    code: int
    message: str
    data: dict
    ex: Exception

    def __init__(
        self,
        *,
        errorDetail: Error.ErrorDetail,
        ex: Exception = None,
    ):
        self.success = False
        self.status_code = errorDetail.status_code
        self.code = errorDetail.code
        self.message = errorDetail.message
        self.data = None
        self.ex = ex
        super().__init__(ex)



class NotAuthenticated(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_authenticated)


class InvalidToken(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.invalid_token)


class EmailAlreadyExist(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.email_already_exist)


class PasswordInvalid(APIException):
    def __init__(self, ex: Exception = None, data: dict | None = None):
        super().__init__(ex=ex, errorDetail=Error.password_invalid)


class NotFoundUser(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_found_user)


class PasswordNotMatch(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.password_not_match)


class NiceApiError(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.nice_api_error)


class NotFoundSchool(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_found_school)


class TooLargeEntity(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.too_large_entity)


class NotRegistSchool(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_regist_school)


class NotFoundStudentList(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_found_student_list)


class NotExistStudentList(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_exist_student_list)


class NotFoundStudent(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_found_student)

class NotFoundColumn(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(ex=ex, errorDetail=Error.not_found_column)


