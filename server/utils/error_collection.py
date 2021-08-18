from rest_framework import status


class ErrorCollection(object):
    def __init__(self, code, status, message):
        self.code = code
        self.status = status
        self.message = message

    def as_md(self):
        return (
            '\n\n> **%s**\n\n```\n{\n\n\t"code": "%s"\n\n\t"message": "%s"\n\n}\n\n```'
            % (self.message, self.code, self.message)
        )


SIGNUP_400_NULL_EMAIL_PASSWORD = ErrorCollection(
    code="SIGNUP_400_INVALID_EMAIL_PASSWORD",
    status=status.HTTP_400_BAD_REQUEST,
    message="이메일 또는 비밀번호를 입력해주세요.",
)
SIGNUP_400_EMAIL_ALREADY_EXIST = ErrorCollection(
    code="SIGNUP_400_EMAIL_ALREADY_EXIST",
    status=status.HTTP_400_BAD_REQUEST,
    message="이미 사용중인 이메일입니다.",
)

SIGNIN_400_NULL_EMAIL_PASSWORD = ErrorCollection(
    code="SIGNIN_400_NULL_EMAIL_PASSWORD",
    status=status.HTTP_400_BAD_REQUEST,
    message="이메일 또는 비밀번호를 입력해주세요.",
)

SIGNIN_401_INVALID_EMAIL_PASSWORD = ErrorCollection(
    code="SIGNUP_400_INVALID_EMAIL_PASSWORD",
    status=status.HTTP_401_UNAUTHORIZED,
    message="이메일이나 비밀번호를 확인해주세요.",
)

KAKAO_400_NOT_FOUND_TOKEN = ErrorCollection(
    code="KAKAO_400_NOT_FOUND_TOKEN",
    status=status.HTTP_400_BAD_REQUEST,
    message="카카오로부터 받은 토큰을 보내주세요.",
)

JWT_403_NOT_FOUND_REFRESHTOKEN = ErrorCollection(
    code="JWT_403_NOT_FOUND_REFRESHTOKEN",
    status=status.HTTP_403_FORBIDDEN,
    message="refresh_token을 보내주세요.",
)

JWT_403_EXPIRED_REFRESHTOKEN = ErrorCollection(
    code="JWT_403_TOKEN_EXPIRED",
    status=status.HTTP_403_FORBIDDEN,
    message="refresh_token이 만료되었습니다.",
)

REVIEW_400_NULL_REQUEST_DATA = ErrorCollection(
    code="REVIEW_400_NULL_REQUEST_DATA",
    status=status.HTTP_400_BAD_REQUEST,
    message="누락된 정보(이미지, 코멘트, 기관ID)가 있습니다. 확인해주세요.",
)

REVIEW_400_ADD_REVIEW_FAILED = ErrorCollection(
    code="REVIEW_400_ADD_REVIEW_FAILED",
    status=status.HTTP_400_BAD_REQUEST,
    message="리뷰 저장 시 문제가 발생했습니다.",
)


DOG_400_ADD_FAILED = ErrorCollection(
    code="DOG_400_ADD_FAILED",
    status=status.HTTP_400_BAD_REQUEST,
    message="유기견 정보 저장 시 문제가 발생했습니다.",
)

DOG_400_MODIFY_FAILED = ErrorCollection(
    code="DOG_400_MODIFY_FAILED",
    status=status.HTTP_400_BAD_REQUEST,
    message="유기견 정보 수정 시 문제가 발생했습니다.",
)
