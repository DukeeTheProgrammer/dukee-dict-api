from django.urls import path
from .views import (
        SearchWord,
        DashBoard,
        api,
        token,
        )


app_name = "dict"

urlpatterns = [
        path("api/search/<str:word>/", SearchWord.as_view(), name="search"),
        path("dashboard/", DashBoard, name="dashboard"),
        path("api/dasboard/", api, name="api"),
        path("token/dashboard/", token, name="token"),
        
        ]
