from django.urls import path
from .views import (
        Login,
        Signup,
        WelcomePage
        )
app_name = "dict_auth"

urlpatterns = [
        path("", WelcomePage.as_view(), name="welocome"),
        path("login/", Login.as_view(), name="login"),
        path("signup/", Signup.as_view(), name="signup"),

        ]
