
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('health', views.change),
    path('health/', views.change_red),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/signin',TokenObtainPairView.as_view()),
    path('users/signup', views.SignUp.as_view()),
    path('users/logout',views.LogoutApiView.as_view()),
    path('users/get',views.users_get),
]
