"""Auth api views"""

from django.conf import settings

from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
)

__all__ = ["TokenPairObtainView", "TokenRefreshObtainView", "VerifyTokenView"]


class TokenPairObtainView(TokenObtainPairView):
    @extend_schema(
        tags=["auth"], responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer}
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get(settings.AUTH_ACCESS_COOKIE)
            refresh_token = response.data.get(settings.AUTH_REFRESH_COOKIE)

            response.set_cookie(
                settings.AUTH_ACCESS_COOKIE,
                access_token,
                max_age=settings.AUTH_ACCESS_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )

            response.set_cookie(
                settings.AUTH_REFRESH_COOKIE,
                refresh_token,
                max_age=settings.AUTH_REFRESH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
        return response


class TokenRefreshObtainView(TokenRefreshView):
    @extend_schema(
        tags=["auth"],
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="invalid or expired refresh token"
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get(settings.AUTH_REFRESH_COOKIE)

        if refresh_token:
            request.data[settings.AUTH_REFRESH_COOKIE] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get(settings.AUTH_ACCESS_COOKIE)
            response.set_cookie(
                settings.AUTH_ACCESS_COOKIE,
                access_token,
                max_age=settings.AUTH_ACCESS_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE,
            )
        return response


class VerifyTokenView(TokenVerifyView):
    @extend_schema(
        tags=["auth"],
        responses={
            status.HTTP_200_OK: {},
            status.HTTP_401_UNAUTHORIZED: TokenVerifyResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        access_token = request.COOKIES.get(settings.AUTH_ACCESS_COOKIE)

        if access_token:
            request.data["token"] = access_token

        return super().post(request, *args, **kwargs)


class TokenPairDestroyView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=["auth"], responses={status.HTTP_204_NO_CONTENT: {}})
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.AUTH_ACCESS_COOKIE)
        response.delete_cookie(settings.AUTH_REFRESH_COOKIE)
        return response
