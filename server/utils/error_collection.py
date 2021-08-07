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

KAKAO_400_NULL_TOKEN = ErrorCollection(
    code="KAKAO_400_NULL_TOKEN",
    status=status.HTTP_400_BAD_REQUEST,
    message="카카오로부터 받은 토큰을 보내주세요.",
)

JWT_400_NULL_TOKEN = ErrorCollection(
    code="JWT_400_NULL_TOKEN",
    status=status.HTTP_400_BAD_REQUEST,
    message="refresh_token을 보내주세요.",
)

JWT_401_TOKEN_EXPIRED = ErrorCollection(
    code="JWT_401_TOKEN_EXPIRED",
    status=status.HTTP_401_UNAUTHORIZED,
    message="refresh_token이 만료되었습니다.",
)