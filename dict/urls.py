from django.urls import path
from .views import (
        GetWord,
        DashBoard,
        api,
        token,
        )


app_name = "dict"

urlpatterns = [
        path("api/search/<str:word>/", GetWord, name="getword"),
        path("dashboard/", DashBoard, name="dashboard"),
        path("api/", api, name="api"),
        path("token/", token, name="token"),
        
        ]
