from django.urls import path
from .views import (
        GetWord,
        DashBoard,
        )


app_name = "dict"

urlpatterns = [
        path("api/search/<str:word>/", GetWord, name="getword"),
        path("dashboard/", DashBoard, name="dashboard"),
        
        ]
