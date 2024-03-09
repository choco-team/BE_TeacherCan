from fastapi import status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError


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
    signin_not_match = ErrorDetail(
        1105, "로그인 정보가 일치하지 않습니다.", status.HTTP_401_UNAUTHORIZED
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


async def request_exception_handelr(request: Request, exc: RequestValidationError):
    path = request.url.path
    error = Error.path.get(path)
    if not error:
        return JSONResponse(
            status_code=Error.request_default_error.status_code,
            content={
                "result": False,
                "code": Error.request_default_error.code,
                "message": Error.request_default_error.message,
                "data": exc.errors(),
            },
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "result": False,
            "code": error.code,
            "message": error.message,
            "data": exc.errors(),
        },
    )


async def response_exception_handelr(request: Request, exc: ResponseValidationError):
    data = {
        "path": request.url.path,
        "method": request.method,
        "path_params": request.path_params or None,
        "query_params": str(request.query_params) or None,
        "body": exc.body if hasattr(exc, "body") else None,
    }
    print("💣 서버 에러 발생!!!!\n", data)
    return JSONResponse(
        status_code=Error.server_error.status_code,
        content={
            "result": False,
            "code": Error.server_error.code,
            "message": Error.server_error.message,
            "data": data,
        },
    )


async def api_exception_handelr(request: Request, exc: "APIException"):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "result": exc.result,
            "code": exc.code,
            "message": exc.message,
            "data": exc.data,
        },
    )


class APIException(Exception):
    result: bool
    status_code: int
    code: int
    message: str
    data: dict
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = Error.default.status_code,
        code: int = Error.default.code,
        message: str = Error.default.message,
        data: dict | None = None,
        ex: Exception = None,
    ):
        self.result = False
        self.status_code = status_code
        self.code = code
        self.message = message
        self.data = data
        self.ex = ex
        super().__init__(ex)


class NotAuthenticated(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_authenticated.status_code,
            code=Error.not_authenticated.code,
            message=Error.not_authenticated.message,
            ex=ex,
        )


class InvalidToken(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.invalid_token.status_code,
            code=Error.invalid_token.code,
            message=Error.invalid_token.message,
            ex=ex,
        )


class EmailAlreadyExist(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.email_already_exist.status_code,
            code=Error.email_already_exist.code,
            message=Error.email_already_exist.message,
            ex=ex,
        )


class PasswordInvalid(APIException):
    def __init__(self, ex: Exception = None, data: dict | None = None):
        super().__init__(
            status_code=Error.password_invalid.status_code,
            code=Error.password_invalid.code,
            message=Error.password_invalid.message,
            ex=ex,
            data=data,
        )


class NotFoundUser(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_found_user.status_code,
            code=Error.not_found_user.code,
            message=Error.not_found_user.message,
            ex=ex,
        )


class SigninNotMatch(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.signin_not_match.status_code,
            code=Error.signin_not_match.code,
            message=Error.signin_not_match.message,
            ex=ex,
        )


class NiceApiError(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.nice_api_error.status_code,
            code=Error.nice_api_error.code,
            message=Error.nice_api_error.message,
            ex=ex,
        )


class NotFoundSchool(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_found_school.status_code,
            code=Error.not_found_school.code,
            message=Error.not_found_school.message,
            ex=ex,
        )


class TooLargeEntity(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.too_large_entity.status_code,
            code=Error.too_large_entity.code,
            message=Error.too_large_entity.message,
            ex=ex,
        )


class NotRegistSchool(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_regist_school.status_code,
            code=Error.not_regist_school.code,
            message=Error.not_regist_school.message,
            ex=ex,
        )


class NotFoundStudentList(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_found_student_list.status_code,
            code=Error.not_found_student_list.code,
            message=Error.not_found_student_list.message,
            ex=ex,
        )


class NotExistStudentList(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_exist_student_list.status_code,
            code=Error.not_exist_student_list.code,
            message=Error.not_exist_student_list.message,
            ex=ex,
        )


class NotFoundStudent(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_found_student.status_code,
            code=Error.not_found_student.code,
            message=Error.not_found_student.message,
            ex=ex,
        )

class NotFoundColumn(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=Error.not_found_column.status_code,
            code=Error.not_found_column.code,
            message=Error.not_found_column.message,
            ex=ex,
        )

