from drf_yasg import openapi
from drf_yasg.openapi import Items

from server.models import *


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

SUCCESS_ADD_USER_REVIEW = Success(
    message="리뷰가 성공적으로 작성되었습니다.",
    data={
        "_id": openapi.Schema(type=openapi.TYPE_STRING, description="리뷰 id"),
        "comment": openapi.Schema(type=openapi.TYPE_STRING, description="리뷰 내용"),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="리뷰 내용",
        ),
        "organization": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="기관 정보",
            properties={
                "_id": openapi.Schema(type=openapi.TYPE_STRING, description="기관 id"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="기관명"),
                "ceo": openapi.Schema(type=openapi.TYPE_STRING, description="CEO"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 설명"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 전화번호"
                ),
                "images": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="이미지",
                    items=Items(
                        type=openapi.TYPE_STRING,
                    ),
                ),
                "donation": openapi.Schema(
                    type=openapi.TYPE_STRING, description="후원계좌"
                ),
                "fax": openapi.Schema(type=openapi.TYPE_STRING, description="팩스"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "sns": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="SNS",
                    items=Items(
                        type=openapi.TYPE_OBJECT,
                    ),
                ),
            },
        ),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="유저 정보",
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="유저 id"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "phone": openapi.Schema(type=openapi.TYPE_STRING, description="전화번호"),
                "passport": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="여권 인증유무", default=False
                ),
            },
        ),
    },
)

SUCCESS_GET_USER_REVIEW = Success(
    message="리뷰를 성공적으로 불러왔습니다.",
    data={
        "_id": openapi.Schema(type=openapi.TYPE_STRING, description="리뷰 id"),
        "comment": openapi.Schema(type=openapi.TYPE_STRING, description="리뷰 내용"),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="리뷰 내용",
        ),
        "organization": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="기관 정보",
            properties={
                "_id": openapi.Schema(type=openapi.TYPE_STRING, description="기관 id"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="기관명"),
                "ceo": openapi.Schema(type=openapi.TYPE_STRING, description="CEO"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 설명"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 전화번호"
                ),
                "images": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="이미지",
                    items=Items(
                        type=openapi.TYPE_STRING,
                    ),
                ),
                "donation": openapi.Schema(
                    type=openapi.TYPE_STRING, description="후원계좌"
                ),
                "fax": openapi.Schema(type=openapi.TYPE_STRING, description="팩스"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "sns": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="SNS",
                    items=Items(
                        type=openapi.TYPE_OBJECT,
                    ),
                ),
            },
        ),
        "user": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="유저 정보",
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="유저 id"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "phone": openapi.Schema(type=openapi.TYPE_STRING, description="전화번호"),
                "passport": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, description="여권 인증유무", default=False
                ),
            },
        ),
    },
)

SUCCESS_GET_DOG_SINGLE = Success(
    message="정보를 성공적으로 불러왔습니다.",
    data={
        "_id": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 id"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 이름"),
        "breed": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 종류"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 상세정보"),
        "date": openapi.Schema(type=openapi.TYPE_STRING, description="출국 마감 날짜"),
        "destination": openapi.Schema(type=openapi.TYPE_STRING, description="도착지 공항"),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="유기견 사진",
        ),
        "organization": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="기관 정보",
            properties={
                "_id": openapi.Schema(type=openapi.TYPE_STRING, description="기관 id"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="기관명"),
                "ceo": openapi.Schema(type=openapi.TYPE_STRING, description="CEO"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 설명"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 전화번호"
                ),
                "images": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="이미지",
                    items=Items(
                        type=openapi.TYPE_STRING,
                    ),
                ),
                "donation": openapi.Schema(
                    type=openapi.TYPE_STRING, description="후원계좌"
                ),
                "fax": openapi.Schema(type=openapi.TYPE_STRING, description="팩스"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "sns": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="SNS",
                    items=Items(
                        type=openapi.TYPE_OBJECT,
                    ),
                ),
            },
        ),
    },
)

SUCCESS_GET_DOG_DEADLINE = Success(
    message="정보를 성공적으로 불러왔습니다.",
    data={
        "_id": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 id"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 이름"),
        "breed": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 종류"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 상세정보"),
        "date": openapi.Schema(type=openapi.TYPE_STRING, description="출국 마감 날짜"),
        "destination": openapi.Schema(type=openapi.TYPE_STRING, description="도착지 공항"),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="유기견 사진",
        ),
        "organization": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="기관 정보",
            properties={
                "_id": openapi.Schema(type=openapi.TYPE_STRING, description="기관 id"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="기관명"),
                "ceo": openapi.Schema(type=openapi.TYPE_STRING, description="CEO"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 설명"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 전화번호"
                ),
                "images": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="이미지",
                    items=Items(
                        type=openapi.TYPE_STRING,
                    ),
                ),
                "donation": openapi.Schema(
                    type=openapi.TYPE_STRING, description="후원계좌"
                ),
                "fax": openapi.Schema(type=openapi.TYPE_STRING, description="팩스"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "sns": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="SNS",
                    items=Items(
                        type=openapi.TYPE_OBJECT,
                    ),
                ),
            },
        ),
    },
)

SUCCESS_GET_DOG_SEARCH = Success(
    message="정보를 성공적으로 불러왔습니다.",
    data={
        "_id": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 id"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 이름"),
        "breed": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 종류"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 상세정보"),
        "date": openapi.Schema(type=openapi.TYPE_STRING, description="출국 마감 날짜"),
        "destination": openapi.Schema(type=openapi.TYPE_STRING, description="도착지 공항"),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="유기견 사진",
        ),
        "organization": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="기관 정보",
            properties={
                "_id": openapi.Schema(type=openapi.TYPE_STRING, description="기관 id"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="기관명"),
                "ceo": openapi.Schema(type=openapi.TYPE_STRING, description="CEO"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 설명"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 전화번호"
                ),
                "images": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="이미지",
                    items=Items(
                        type=openapi.TYPE_STRING,
                    ),
                ),
                "donation": openapi.Schema(
                    type=openapi.TYPE_STRING, description="후원계좌"
                ),
                "fax": openapi.Schema(type=openapi.TYPE_STRING, description="팩스"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "sns": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="SNS",
                    items=Items(
                        type=openapi.TYPE_OBJECT,
                    ),
                ),
            },
        ),
    },
)

SUCCESS_ADD_DOG_INFO = Success(
    message="정보를 성공적으로 저장하였습니다.",
    data={
        "_id": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 id"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 이름"),
        "breed": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 종류"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 상세정보"),
        "date": openapi.Schema(type=openapi.TYPE_STRING, description="출국 마감 날짜"),
        "destination": openapi.Schema(type=openapi.TYPE_STRING, description="도착지 공항"),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="유기견 사진",
        ),
        "organization": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="기관 정보",
            properties={
                "_id": openapi.Schema(type=openapi.TYPE_STRING, description="기관 id"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="기관명"),
                "ceo": openapi.Schema(type=openapi.TYPE_STRING, description="CEO"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 설명"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 전화번호"
                ),
                "images": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="이미지",
                    items=Items(
                        type=openapi.TYPE_STRING,
                    ),
                ),
                "donation": openapi.Schema(
                    type=openapi.TYPE_STRING, description="후원계좌"
                ),
                "fax": openapi.Schema(type=openapi.TYPE_STRING, description="팩스"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "sns": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="SNS",
                    items=Items(
                        type=openapi.TYPE_OBJECT,
                    ),
                ),
            },
        ),
    },
)

SUCCESS_DELETE_DOG_SINGLE = Success(
    message="정보를 성공적으로 삭제하였습니다.",
    data={
        "_id": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 id"),
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 이름"),
        "breed": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 종류"),
        "description": openapi.Schema(type=openapi.TYPE_STRING, description="유기견 상세정보"),
        "date": openapi.Schema(type=openapi.TYPE_STRING, description="출국 마감 날짜"),
        "destination": openapi.Schema(type=openapi.TYPE_STRING, description="도착지 공항"),
        "image": openapi.Schema(
            type=openapi.TYPE_STRING,
            description="유기견 사진",
        ),
        "organization": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            description="기관 정보",
            properties={
                "_id": openapi.Schema(type=openapi.TYPE_STRING, description="기관 id"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="기관명"),
                "ceo": openapi.Schema(type=openapi.TYPE_STRING, description="CEO"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 설명"
                ),
                "phone": openapi.Schema(
                    type=openapi.TYPE_STRING, description="기관 전화번호"
                ),
                "images": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="이미지",
                    items=Items(
                        type=openapi.TYPE_STRING,
                    ),
                ),
                "donation": openapi.Schema(
                    type=openapi.TYPE_STRING, description="후원계좌"
                ),
                "fax": openapi.Schema(type=openapi.TYPE_STRING, description="팩스"),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "sns": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="SNS",
                    items=Items(
                        type=openapi.TYPE_OBJECT,
                    ),
                ),
            },
        ),
    },
)
