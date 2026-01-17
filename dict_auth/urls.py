from django.urls import path
from .views import (
        Login,
        Signup,
        WelcomePage,
        Logout,
        ForgotPassword,
        )
app_name = "dict_auth"

urlpatterns = [
        path("", WelcomePage.as_view(), name="welocome"),
        path("login/", Login.as_view(), name="login"),
        path("logout/", Logout.as_view(), name="logout"),
        path("signup/", Signup.as_view(), name="signup"),
        path("forgot/password/", ForgotPassword.as_view(), name="forgot_password"),

        ]
