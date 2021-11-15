from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [

path('', views.ClassList.as_view()),
path('/', views.ClassList.as_view()),
path('/<int:pk>', views.ClassListDetail.as_view()),
]