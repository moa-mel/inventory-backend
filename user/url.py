from django.urls import path

from user.views import ActivateAccountView, RegisterView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path(
        "activate/",
        ActivateAccountView.as_view(),
        name="activate-account",
    ),
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    
]