"Auth Api Serializers"

"""Auth api serializers"""

from rest_framework import serializers


__all__ = [
    "TokenObtainPairResponseSerializer",
    "TokenRefreshResponseSerializer",
    "TokenVerifyResponseSerializer",
]


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class TokenVerifyResponseSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=128)
    code = serializers.CharField(max_length=128)
