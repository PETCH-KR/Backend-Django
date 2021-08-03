from drf_yasg import openapi


class Success(object):
    def __init__(self, message, data):
        self.message = message
        self.data = openapi.Schema(
            "data", description="데이터", type=openapi.TYPE_OBJECT, properties=data
        )

    def as_obj(self):
        success_field = openapi.Schema(
            "success", description="성공 여부", type=openapi.TYPE_BOOLEAN, default=True
        )
        message_field = openapi.Schema(
            "message", description=self.message, type=openapi.TYPE_STRING
        )
        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "success": success_field,
                "message": message_field,
                "data": self.data,
            },
        )


SUCCESS_SIGNUP = Success(
    message="회원가입에 성공했습니다.",
    data={
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="유저데이터",
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
            },
        ),
    },
)

SUCCESS_SIGNIN = Success(
    message="로그인에 성공했습니다.",
    data={
        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="리프레시 토큰"
        ),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
    },
)

SUCCESS_KAKAO = Success(
    message="카카오 로그인에 성공했습니다.",
    data={
        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="리프레시 토큰"
        ),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
    },
)

SUCCESS_REFRESH_TOKEN = Success(
    message="access_token이 재발급되었습니다.",
    data={
        "access_token": openapi.Schema(type=openapi.TYPE_STRING, description="액세스 토큰"),
        "refresh_token": openapi.Schema(
            type=openapi.TYPE_STRING, description="리프레시 토큰"
        ),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
    },
)
