class DefaultError(Exception):
    def __init__(self, status_code=500, code=1000, message=""):
        self.status_code = status_code
        self.code = code
        self.message = message


# Auth
invalid_token = DefaultError(401, 1002, "유효하지 않은 토큰이에요.")
email_already_exist = DefaultError(409, 1102, "이메일이 이미 존재해요.")

#     # School
#     nice_api_error = DefaultError(
#         1301, "관련된 정보를 불러오는 중에 에러가 발생했어요.", status.HTTP_503_SERVICE_UNAVAILABLE
#     )
#     not_found_school = DefaultError(
#         1302, "해당하는 학교 정보가 존재하지 않아요.", status.HTTP_404_NOT_FOUND
#     )
#     too_large_entity = DefaultError(
#         1303, "데이터 요청은 한번에 1,000건을 넘을 수 없어요.", status.HTTP_400_BAD_REQUEST
#     )
#     not_regist_school = DefaultError(
#         1304, "등록된 학교 정보가 없어요. 먼저 학교를 등록해주세요.", status.HTTP_404_NOT_FOUND
#     )

#     # Student
#     not_found_student_list = DefaultError(
#         1401, "요청하신 명렬표가 존재하지 않아요.", status.HTTP_404_NOT_FOUND
#     )
#     not_exist_student_list = DefaultError(
#         1402, "등록된 명렬표가 없어요. 먼저 명렬표를 등록해주세요.", status.HTTP_404_NOT_FOUND
#     )
#     not_found_student = DefaultError(
#         1403, "해당하는 학생이 존재하지 않아요.", status.HTTP_404_NOT_FOUND
#     )

#     #Column
#     not_found_column = DefaultError(
#         1501, "요청하신 column이 존재하지 않아요.", status.HTTP_404_NOT_FOUND
#     )

#     # 유효성 검사
#     request_default_error = DefaultError(
#         1003, "유효성 검사에서 문제가 발생했어요.", status.HTTP_400_BAD_REQUEST
#     )
#     path = {
#         "/api/auth/signup/validation": DefaultError(1101, "이메일이 형식이 올바르지 않아요."),
#     }
