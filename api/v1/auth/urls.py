from django.urls import path

from .views import (
    TokenPairObtainView,
    TokenRefreshObtainView,
    VerifyTokenView,
    TokenPairDestroyView,
)

urlpatterns = [
    path("tokens", TokenPairObtainView.as_view(), name="user-tokens"),
    path("tokens/refresh", TokenRefreshObtainView.as_view(), name="generate-token"),
    path("tokens/verify", VerifyTokenView.as_view(), name="verify-token"),
    path("tokens/delete", TokenPairDestroyView.as_view(), name="delete-tokens"),
]
