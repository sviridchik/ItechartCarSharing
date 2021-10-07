from cars.urls import pk_reg
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

app_name = "class"

urlpatterns = [
    path('/', views.ClassList.as_view(), name="list"),
    re_path(pk_reg, views.ClassListDetail.as_view(), name="pk")
]
